
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from PIL import Image, ImageOps
from io import BytesIO

# ==========================================
# 1. 페이지 설정
# ==========================================

st.set_page_config(
    page_title="녹조 제거 효과 분석기",
    page_icon="🌿",
    layout="wide"
)

st.title("🌿 녹조 제거 효과 분석기")
st.write(
    "ImageJ 기반 이미지 분석과 실험 데이터를 활용하여 "
    "녹조 농도 및 응집제 투여량을 비교하는 앱입니다."
)

st.warning(
    "이 앱의 투여량은 실험 기준점에 비례한 초기 추정값입니다. "
    "실제 녹조 제거율이나 최적 투여량을 보장하지 않습니다."
)

# ==========================================
# 2. 기준 실험 설정
# ==========================================

st.sidebar.header("기준 실험 설정")

ref_algae_pct = st.sidebar.number_input(
    "기준 녹조 농도 (%)",
    min_value=0.01,
    max_value=100.0,
    value=1.0,
    step=0.1
)

ref_sample_ml = st.sidebar.number_input(
    "기준 녹조 시료 부피 (mL)",
    min_value=0.1,
    max_value=100000.0,
    value=10.0,
    step=1.0,
    help="임시 기본값입니다. 실제 실험의 시료 부피로 수정하세요."
)

ref_alum_ml = st.sidebar.number_input(
    "기준 황산알루미늄 용액 (mL)",
    min_value=0.0,
    max_value=10000.0,
    value=0.5,
    step=0.1
)

ref_moringa_ml = st.sidebar.number_input(
    "기준 모링가 씨앗 용액 (mL)",
    min_value=0.0,
    max_value=10000.0,
    value=0.5,
    step=0.1
)

st.sidebar.caption(
    "기준점: 녹조 1%에서 황산알루미늄 0.5mL + "
    "모링가 용액 0.5mL"
)

# ==========================================
# 3. 탭 구성
# ==========================================

tab1, tab2, tab3 = st.tabs([
    "① 투여량 계산",
    "② 사진 명암 분석",
    "③ 엑셀 실험 결과"
])

# ==========================================
# 4. 투여량 계산
# ==========================================

with tab1:

    st.header("녹조 농도별 응집제 투여량 계산")

    col1, col2 = st.columns(2)

    with col1:
        algae_pct = st.number_input(
            "현재 녹조 농도 (%)",
            min_value=0.01,
            max_value=100.0,
            value=2.0,
            step=0.1
        )

        sample_ml = st.number_input(
            "처리할 녹조 시료 부피 (mL)",
            min_value=0.1,
            max_value=100000.0,
            value=10.0,
            step=1.0
        )

    with col2:
        ratio_mode = st.selectbox(
            "응집제 혼합 비율",
            [
                "1:1 (기준 비율)",
                "황산알루미늄 3 : 모링가 7",
                "황산알루미늄 7 : 모링가 3",
                "황산알루미늄만",
                "모링가만"
            ]
        )

        st.caption(
            "혼합비는 황산알루미늄 : 모링가 순서입니다."
        )

    # 농도와 시료 부피에 비례하는 초기 추정식
    concentration_factor = algae_pct / ref_algae_pct
    volume_factor = sample_ml / ref_sample_ml

    scale_factor = concentration_factor * volume_factor

    reference_total = ref_alum_ml + ref_moringa_ml
    estimated_total = reference_total * scale_factor

    # 혼합비 결정
    if ratio_mode == "1:1 (기준 비율)":
        alum_ratio = 0.5
        moringa_ratio = 0.5

    elif ratio_mode == "황산알루미늄 3 : 모링가 7":
        alum_ratio = 0.3
        moringa_ratio = 0.7

    elif ratio_mode == "황산알루미늄 7 : 모링가 3":
        alum_ratio = 0.7
        moringa_ratio = 0.3

    elif ratio_mode == "황산알루미늄만":
        alum_ratio = 1.0
        moringa_ratio = 0.0

    else:
        alum_ratio = 0.0
        moringa_ratio = 1.0

    # 각각의 투여량
    dose_alum = estimated_total * alum_ratio
    dose_moringa = estimated_total * moringa_ratio

    # 결과 출력
    st.subheader("계산 결과")

    m1, m2, m3 = st.columns(3)

    m1.metric(
        "황산알루미늄 용액",
        f"{dose_alum:.3f} mL"
    )

    m2.metric(
        "모링가 씨앗 용액",
        f"{dose_moringa:.3f} mL"
    )

    m3.metric(
        "총 투여량",
        f"{dose_alum + dose_moringa:.3f} mL"
    )

    st.info(
        f"농도 배율: {concentration_factor:.3f}배\n\n"
        f"시료 부피 배율: {volume_factor:.3f}배\n\n"
        f"최종 투여 배율: {scale_factor:.3f}배"
    )

    st.markdown("### 계산식")

    st.latex(
        r"D = D_0 \times "
        r"\frac{C}{C_0} \times "
        r"\frac{V}{V_0}"
    )

    st.write(
        "D: 추정 투여량, D₀: 기준 투여량, "
        "C: 현재 농도, C₀: 기준 농도, "
        "V: 현재 시료 부피, V₀: 기준 시료 부피"
    )

    st.caption(
        "이 계산식은 농도와 시료 부피에 선형 비례한다고 가정합니다. "
        "실제 응집 반응은 비선형일 수 있으므로 여러 투여량으로 "
        "추가 실험을 진행해야 합니다."
    )

    # CSV 저장
    result_df = pd.DataFrame({
        "항목": [
            "현재 녹조 농도",
            "현재 시료 부피",
            "혼합 비율",
            "황산알루미늄 추정량",
            "모링가 추정량",
            "총 추정량",
            "투여 배율"
        ],
        "값": [
            f"{algae_pct}%",
            f"{sample_ml}mL",
            ratio_mode,
            f"{dose_alum:.3f}mL",
            f"{dose_moringa:.3f}mL",
            f"{estimated_total:.3f}mL",
            f"{scale_factor:.3f}"
        ]
    })

    st.download_button(
        label="계산 결과 CSV 다운로드",
        data=result_df.to_csv(
            index=False
        ).encode("utf-8-sig"),
        file_name="녹조_투여량_계산결과.csv",
        mime="text/csv"
    )

# ==========================================
# 5. 사진 명암 분석
# ==========================================

with tab2:

    st.header("처리 전후 녹조 사진 분석")

    st.write(
        "처리 전후 사진의 RGB 평균과 초록색 지표를 비교합니다. "
        "실제 녹조 농도(%)를 판정하려면 별도의 농도 보정 실험이 필요합니다."
    )

    col_before, col_after = st.columns(2)

    with col_before:
        before_file = st.file_uploader(
            "처리 전 사진 업로드",
            type=["png", "jpg", "jpeg", "tif", "tiff"],
            key="before_image"
        )

    with col_after:
        after_file = st.file_uploader(
            "처리 후 사진 업로드",
            type=["png", "jpg", "jpeg", "tif", "tiff"],
            key="after_image"
        )

    def analyze_image(uploaded_file):
        """
        이미지 RGB 평균과 Excess Green 지표 계산.
        픽셀값은 0~255 범위로 변환하여 출력한다.
        """

        image = Image.open(uploaded_file)
        image = ImageOps.exif_transpose(image)
        image = image.convert("RGB")

        arr = np.asarray(image, dtype=np.float32) / 255.0

        red = arr[:, :, 0]
        green = arr[:, :, 1]
        blue = arr[:, :, 2]

        mean_red = float(np.mean(red) * 255)
        mean_green = float(np.mean(green) * 255)
        mean_blue = float(np.mean(blue) * 255)

        # Excess Green = 2G - R - B
        excess_green = 2 * green - red - blue
        mean_excess_green = float(np.mean(excess_green))

        metrics = {
            "평균 R": mean_red,
            "평균 G (Mean Green)": mean_green,
            "평균 B": mean_blue,
            "평균 Excess Green": mean_excess_green,
            "이미지 너비": image.width,
            "이미지 높이": image.height
        }

        return image, metrics

    if before_file is not None and after_file is not None:

        img_before, metrics_before = analyze_image(before_file)
        img_after, metrics_after = analyze_image(after_file)

        p1, p2 = st.columns(2)

        with p1:
            st.image(
                img_before,
                caption="처리 전 이미지",
                use_container_width=True
            )

            st.write("처리 전 측정값")

            st.dataframe(
                pd.DataFrame(
                    metrics_before.items(),
                    columns=["측정 항목", "값"]
                ),
                use_container_width=True
            )

        with p2:
            st.image(
                img_after,
                caption="처리 후 이미지",
                use_container_width=True
            )

            st.write("처리 후 측정값")

            st.dataframe(
                pd.DataFrame(
                    metrics_after.items(),
                    columns=["측정 항목", "값"]
                ),
                use_container_width=True
            )

        # 평균 초록색 채널의 변화
        green_before = metrics_before["평균 G (Mean Green)"]
        green_after = metrics_after["평균 G (Mean Green)"]

        green_change = green_after - green_before

        if green_before != 0:
            green_relative_change = (
                (green_before - green_after) / green_before
            ) * 100
        else:
            green_relative_change = np.nan

        excess_change = (
            metrics_after["평균 Excess Green"]
            - metrics_before["평균 Excess Green"]
        )

        st.subheader("처리 전후 비교")

        q1, q2, q3 = st.columns(3)

        q1.metric(
            "Mean Green 변화",
            f"{green_change:+.2f}"
        )

        q2.metric(
            "Mean Green 상대 감소율",
            (
                f"{green_relative_change:.2f}%"
                if np.isfinite(green_relative_change)
                else "계산 불가"
            )
        )

        q3.metric(
            "Excess Green 변화",
            f"{excess_change:+.4f}"
        )

        st.warning(
            "Mean Green 상대 감소율은 이미지의 초록색 채널 변화율이며 "
            "실제 녹조 제거율과 같지 않습니다. 침전으로 녹조가 가라앉으면 "
            "촬영 위치에 따라서도 값이 달라질 수 있습니다."
        )

        # 결과를 CSV로 저장
        image_result_df = pd.DataFrame({
            "측정 항목": list(metrics_before.keys()),
            "처리 전": list(metrics_before.values()),
            "처리 후": list(metrics_after.values())
        })

        image_result_df = pd.concat(
            [
                image_result_df,
                pd.DataFrame({
                    "측정 항목": [
                        "Mean Green 변화",
                        "Mean Green 상대 감소율 (%)",
                        "Excess Green 변화"
                    ],
                    "처리 전": [
                        np.nan,
                        np.nan,
                        np.nan
                    ],
                    "처리 후": [
                        green_change,
                        green_relative_change,
                        excess_change
                    ]
                })
            ],
            ignore_index=True
        )

        st.download_button(
            "이미지 분석 결과 CSV 다운로드",
            data=image_result_df.to_csv(
                index=False
            ).encode("utf-8-sig"),
            file_name="녹조_이미지_분석결과.csv",
            mime="text/csv"
        )

    else:
        st.info(
            "처리 전 사진과 처리 후 사진을 모두 업로드하면 "
            "명암 분석 결과를 확인할 수 있습니다."
        )

    st.divider()

    st.subheader("ImageJ 측정 CSV 불러오기")

    st.write(
        "ImageJ/Fiji에서 측정한 CSV 파일이 있다면 업로드할 수 있습니다."
    )

    imagej_file = st.file_uploader(
        "ImageJ 측정 CSV 업로드",
        type=["csv"],
        key="imagej_csv"
    )

    if imagej_file is not None:

        try:
            imagej_df = pd.read_csv(imagej_file)

            st.dataframe(
                imagej_df,
                use_container_width=True
            )

            st.download_button(
                "ImageJ 데이터 CSV 저장",
                data=imagej_df.to_csv(
                    index=False
                ).encode("utf-8-sig"),
                file_name="ImageJ_측정데이터.csv",
                mime="text/csv"
            )

        except Exception as error:
            st.error(
                f"CSV 파일을 읽는 중 오류가 발생했습니다: {error}"
            )

    st.markdown("### ImageJ/Fiji 측정 방법")

    st.markdown(
        """
        1. ImageJ/Fiji에서 녹조 사진을 엽니다.
        2. `Image → Color → Split Channels`로 RGB 채널을 분리합니다.
        3. 초록색 채널에서 분석할 시료 영역(ROI)을 동일하게 선택합니다.
        4. `Analyze → Set Measurements`에서 Mean gray value를 선택합니다.
        5. `Analyze → Measure`로 평균값을 기록합니다.
        6. 처리 전후 사진을 같은 조명, 노출, 배경, 촬영 거리로 비교합니다.
        """
    )

# ==========================================
# 6. 엑셀 실험 결과 분석
# ==========================================

with tab3:

    st.header("실험 결과 엑셀 분석")

    st.write(
        "제공된 실험 그래프의 시간별 Mean Green Value를 비교합니다. "
        "새로운 엑셀 파일을 올려 분석할 수도 있습니다."
    )

    # 제공된 그래프에서 읽은 값
    default_data = pd.DataFrame({
        "시간": [
            "교반 전",
            "교반 직후",
            "5분 후",
            "10분 후",
            "15분 후"
        ],

        "황산알루미늄 10mL": [
            30.135, 73.769, 61.902, 60.990, 56.710
        ],

        "황산알루미늄 3mL + 모링가 7mL": [
            67.164, 40.990, 83.348, 50.708, 68.895
        ],

        "황산알루미늄 5mL + 모링가 5mL": [
            48.935, 56.039, 76.293, 63.127, 81.166
        ],

        "황산알루미늄 7mL + 모링가 3mL": [
            53.199, 53.199, 63.484, 64.789, 59.610
        ],

        "모링가 10mL": [
            38.063, 26.813, 44.850, 57.144, 54.348
        ]
    })

    excel_file = st.file_uploader(
        "실험 엑셀 파일 업로드",
        type=["xlsx", "xls"],
        key="experiment_excel"
    )

    if excel_file is not None:

        try:
            xls = pd.ExcelFile(excel_file)

            sheet_name = st.selectbox(
                "분석할 시트 선택",
                options=xls.sheet_names
            )

            experiment_df = pd.read_excel(
                excel_file,
                sheet_name=sheet_name
            )

            st.subheader("엑셀 데이터")

            st.dataframe(
                experiment_df,
                use_container_width=True
            )

            st.caption(
                "업로드한 데이터는 표로 표시합니다. "
                "시간과 측정값이 포함된 열을 확인한 후 그래프를 작성하세요."
            )

            numeric_columns = experiment_df.select_dtypes(
                include=np.number
            ).columns.tolist()

            if len(numeric_columns) >= 1:

                value_column = st.selectbox(
                    "그래프로 표시할 측정값 열",
                    options=numeric_columns
                )

                fig, ax = plt.subplots(figsize=(10, 4))

                ax.plot(
                    range(len(experiment_df)),
                    experiment_df[value_column],
                    marker="o"
                )

                ax.set_title(value_column)
                ax.set_xlabel("측정 순서")
                ax.set_ylabel("측정값")
                ax.grid(True, alpha=0.3)

                st.pyplot(fig)

            else:
                st.info(
                    "그래프를 만들 수 있는 숫자형 열이 없습니다."
                )

        except Exception as error:
            st.error(
                f"엑셀 파일을 읽는 중 오류가 발생했습니다: {error}"
            )

    else:

        st.subheader("기존 실험 데이터")

        st.dataframe(
            default_data,
            use_container_width=True
        )

        # 전체 실험 조건을 하나의 그래프에 표시
        fig, ax = plt.subplots(figsize=(11, 5))

        for column in default_data.columns[1:]:

            ax.plot(
                default_data["시간"],
                default_data[column],
                marker="o",
                label=column
            )

        ax.set_title("시간별 Mean Green Value 비교")
        ax.set_xlabel("측정 시간")
        ax.set_ylabel("Mean Green Value")
        ax.grid(True, alpha=0.3)

        ax.legend(
            fontsize=8,
            ncol=2
        )

        plt.xticks(rotation=0)
        plt.tight_layout()

        st.pyplot(fig)

        st.caption(
            "위 값은 제공된 그래프에서 읽어 입력한 예시 데이터입니다. "
            "원본 엑셀 시트와 대조하여 필요한 값을 수정하세요."
        )

        st.download_button(
            "기존 실험 데이터 CSV 다운로드",
            data=default_data.to_csv(
                index=False
            ).encode("utf-8-sig"),
            file_name="녹조_실험데이터.csv",
            mime="text/csv"
        )

# ==========================================
# 7. 앱 하단 안내
# ==========================================

st.divider()

st.subheader("실험 결과를 더 정확하게 만드는 방법")

st.markdown(
    """
    - 같은 농도와 같은 시료 부피에서 용액 투여량을 여러 단계로 시험합니다.
    - 각 조건을 3회 이상 반복하고 평균과 표준편차를 기록합니다.
    - 사진의 조명, 배경, 노출, 용기, 촬영 거리를 동일하게 유지합니다.
    - ImageJ에서 같은 크기의 ROI를 사용하고 배경을 제외합니다.
    - 이미지 지표를 실제 녹조 농도 측정값과 연결해 보정 곡선을 만듭니다.
    - 검증된 데이터가 충분히 모이면 단순 비례식 대신 회귀 모델을 적용합니다.
    """
)

st.caption(
    "교육 및 실험 분석용 앱입니다. 실제 수질 처리나 환경 방류를 위한 "
    "투여량은 별도의 실험 및 전문가 검증이 필요합니다."
)
