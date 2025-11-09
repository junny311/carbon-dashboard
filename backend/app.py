from flask import Flask, jsonify, render_template
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__, template_folder='../frontend', static_folder='../frontend/assets')
CORS(app)

DATA_DIR = "data"

# API: 차량 탄소배출량
@app.route("/api/emissions/vehicle", methods=['GET'])
def vehicle_emissions():
    df = pd.read_csv(os.path.join(DATA_DIR, "vehicle.csv"))
    df["탄소배출량"] = (df["주행거리"] / df["연비"]) * df["배출계수"] * df["차량수"]
    result = df.groupby("날짜")["탄소배출량"].sum().reset_index()
    result["탄소배출량"] = result["탄소배출량"].round(2)
    return jsonify(result.to_dict(orient="records"))

# API: 차량 연료별 탄소배출량
@app.route("/api/emissions/vehicle/by-fuel", methods=["GET"])
def vehicle_emissions_by_fuel():
    df = pd.read_csv(os.path.join(DATA_DIR, "vehicle.csv"))
    df["탄소배출량"] = (df["주행거리"] / df["연비"]) * df["배출계수"] * df["차량수"]
    result = df.groupby(["날짜", "연료 종류"])["탄소배출량"].sum().reset_index()
    result["탄소배출량"] = result["탄소배출량"].round(2)
    fuel_data = {}
    for fuel in result["연료 종류"].unique():
        records = result[result["연료 종류"] == fuel][["날짜", "탄소배출량"]].to_dict(orient="records")
        if any(record["탄소배출량"] > 0 for record in records):
            fuel_data[fuel] = records
    return jsonify(fuel_data)

@app.route("/api/emissions/vehicle/monthly", methods=["GET"])
def vehicle_emissions_monthly():
    """vehicle3.csv를 사용한 월별 탄소배출량 계산"""
    filepath = os.path.join(DATA_DIR, "vehicle3.csv")
    if not os.path.exists(filepath):
        return jsonify({"error": "vehicle3.csv file not found."}), 404

    df = pd.read_csv(filepath)
    df["탄소배출량"] = (df["주행거리"] / df["연비"]) * df["배출계수"] * df["차량수"]
    
    # 날짜별로 그룹화하여 월별 총 배출량 계산
    result = df.groupby("날짜")["탄소배출량"].sum().reset_index()
    result["탄소배출량"] = result["탄소배출량"].round(2)
    
    return jsonify(result.to_dict(orient="records"))

# API: 폐기물 탄소배출량 (CH4를 CO2eq로 변환)
@app.route("/api/emissions/waste/by-type", methods=["GET"])
def waste_emissions_by_type():
    df = pd.read_csv(os.path.join(DATA_DIR, "waste.csv"))
    df["탄소배출량"] = 0.0

    # 의료폐기물 - 매립 (CH4 계산 후 CO2eq로 변환)
    mask1 = (df["종류"] == "의료폐기물") & (df["처리방식"] == "매립")
    df.loc[mask1, "탄소배출량"] = (
        df.loc[mask1, "MSW"] * 
        df.loc[mask1, "DOC"] * 
        df.loc[mask1, "DOCj"] * 
        df.loc[mask1, "MCF"] * 
        df.loc[mask1, "F"] * 
        (16 / 12) * 
        (1 - df.loc[mask1, "R"]) * 
        28  # CH4를 CO2eq로 변환
    )

    # 의료폐기물 - 소각 (kg CO2eq로 변환)
    mask2 = (df["종류"] == "의료폐기물") & (df["처리방식"] == "소각")
    df.loc[mask2, "탄소배출량"] = (
        df.loc[mask2, "MSW"] * 
        df.loc[mask2, "소각배출계수"] * 
        28  # kg CO2eq로 변환
    )

    # 지정폐기물 (CH4 계산 후 CO2eq로 변환)
    mask3 = (df["종류"] == "지정폐기물")
    df.loc[mask3, "탄소배출량"] = (
        df.loc[mask3, "MSW"] * 
        df.loc[mask3, "DOC"] * 
        df.loc[mask3, "DOCj"] * 
        df.loc[mask3, "MCF"] * 
        df.loc[mask3, "F"] * 
        (16 / 12) * 
        (1 - df.loc[mask3, "R"]) * 
        28  # CH4를 CO2eq로 변환
    )

    # 산업폐수 (CH4 계산 후 CO2eq로 변환)
    mask4 = (df["종류"] == "산업폐수")
    df.loc[mask4, "탄소배출량"] = (
        df.loc[mask4, "TOW"] * 
        df.loc[mask4, "EF"] * 
        (1 - df.loc[mask4, "R"]) * 
        28  # CH4를 CO2eq로 변환
    )

    result = df.groupby(["날짜", "종류"])["탄소배출량"].sum().reset_index()
    result["탄소배출량"] = result["탄소배출량"].round(4)

    return jsonify({
        "의료폐기물": result[result["종류"] == "의료폐기물"][["날짜", "탄소배출량"]].to_dict(orient="records"),
        "지정폐기물": result[result["종류"] == "지정폐기물"][["날짜", "탄소배출량"]].to_dict(orient="records"),
        "산업폐수": result[result["종류"] == "산업폐수"][["날짜", "탄소배출량"]].to_dict(orient="records")
    })

# API: 녹지 탄소 흡수량/저장량
@app.route("/api/emissions/greenery/details", methods=["GET"])
def greenery_details():
    result = {
        "summary": {"총_녹지_면적": 0, "총_수목_수": 0, "연간_탄소_저장량": 0, "연간_탄소_흡수량": 0},
        "tree_data": [],
        "area_data": []
    }

    try:
        # 나무별 총 흡수량 계산
        total_tree_absorption = 0  # 나무별 흡수량 총합
        
        tree_path = os.path.join(DATA_DIR, "greenery_tree.csv")
        if os.path.exists(tree_path):
            df_tree = pd.read_csv(tree_path)
            
            result["summary"]["총_수목_수"] = int(df_tree["개체수"].sum())
            
            # 나무별 계산 (면적 0.002ha 추가)
            for _, row in df_tree.iterrows():
                tree_name = str(row["수종명"])
                tree_count = int(row["개체수"])
                
                # 각 값 추출
                delta_v = float(row["ΔV"])
                d = float(row["D"])  
                bef = float(row["BEF"])
                r = float(row["R"])
                cf = float(row["CF"])
                
                # 수정된 계산: 면적 0.002ha 추가
                unit_absorption_per_ha = delta_v * d * bef * (1 + r) * cf * (44 / 12)
                unit_absorption_per_tree = unit_absorption_per_ha * 0.002  # 1그루당 0.002ha
                tree_total_absorption = unit_absorption_per_tree * tree_count
                
                result["tree_data"].append({
                    "수종명": tree_name,
                    "개체수": tree_count,
                    "탄소흡수량": round(tree_total_absorption, 4)
                })
                
                # 나무별 흡수량 총합에 추가
                total_tree_absorption += tree_total_absorption
                result["summary"]["연간_탄소_흡수량"] += tree_total_absorption

        # 면적 기반 데이터
        area_path = os.path.join(DATA_DIR, "greenery_area.csv")
        if os.path.exists(area_path):
            df_area = pd.read_csv(area_path)
            
            result["summary"]["총_녹지_면적"] = float(df_area["면적(m²)"].sum())
            
            for _, row in df_area.iterrows():
                if row["구분"] == "Land Area":
                    absorption = float(row["면적(m²)"]) * float(row["carbon_uptake"])
                    storage = float(row["면적(m²)"]) * float(row["carbon_storage"])
                    result["summary"]["연간_탄소_저장량"] += storage
                    result["area_data"].append({
                        "구분": "비수관면적 (땅)",
                        "흡수량": round(absorption, 2),
                        "저장량": round(storage, 2)
                    })
                elif row["구분"] == "Tree Cover":
                    storage = float(row["면적(m²)"]) * float(row["carbon_storage"])
                    result["summary"]["연간_탄소_저장량"] += storage
                    
                    # 수관면적의 흡수량을 나무별 흡수량 총합으로 교체
                    result["area_data"].append({
                        "구분": "수관면적 (나무)",
                        "흡수량": round(total_tree_absorption, 2),  # 나무별 총합 사용
                        "저장량": round(storage, 2)
                    })

        # 반올림
        result["summary"]["총_녹지_면적"] = round(result["summary"]["총_녹지_면적"], 0)
        result["summary"]["연간_탄소_저장량"] = round(result["summary"]["연간_탄소_저장량"], 2)
        result["summary"]["연간_탄소_흡수량"] = round(result["summary"]["연간_탄소_흡수량"], 4)

        return jsonify(result)
        
    except Exception as e:
        return jsonify({"error": f"데이터 처리 중 오류: {str(e)}"}), 500

# API: 물 사용 탄소배출량
@app.route("/api/emissions/water", methods=["GET"])
def water_emissions():
    df = pd.read_csv(os.path.join(DATA_DIR, "water.csv"))
    df["탄소배출량"] = df["총량"] * df["전력원단위"] * df["배출계수"]
    result = df[["날짜", "탄소배출량"]].copy()
    result["탄소배출량"] = result["탄소배출량"].round(2)
    return jsonify(result.to_dict(orient="records"))

# API: 전력 사용 탄소배출량
@app.route("/api/emissions/electric/detailed", methods=["GET"])
def electric_emissions_detailed():
    df = pd.read_csv(os.path.join(DATA_DIR, "electric.csv"))
    if '배출계수' in df.columns:
        df["탄소배출량"] = df["총 사용 전력량"] * df["배출계수"]
    else:
        df["탄소배출량"] = df["총 사용 전력량"] * 0.4517  # default 계수
    return jsonify(df.to_dict(orient="records"))

# 서버 실행
if __name__ == '__main__':
    app.run(debug=True, port=5173)