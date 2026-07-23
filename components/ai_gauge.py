import streamlit as st
import plotly.graph_objects as go


def ai_gauge(probability):

    if probability is None:
        return

    percent = round(probability * 100, 1)

    if percent < 40:
        color = "#22C55E"
        status = "LOW RISK"

    elif percent < 70:
        color = "#F59E0B"
        status = "MODERATE"

    else:
        color = "#EF4444"
        status = "HIGH RISK"

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=percent,

            number={
                "suffix": "%",
                "font": {
                    "size": 42,
                    "color": "white"
                }
            },

            title={
                "text": f"<b>{status}</b>",
                "font": {
                    "size": 24,
                    "color": color
                }
            },

            gauge={

                "axis": {
                    "range": [0, 100],
                    "tickcolor": "white",
                    "tickfont": {
                        "color": "white"
                    }
                },

                "bar": {
                    "color": color,
                    "thickness": 0.35
                },

                "bgcolor": "#162033",

                "borderwidth": 0,

                "steps": [

                    {
                        "range": [0, 40],
                        "color": "#1F3D2D"
                    },

                    {
                        "range": [40, 70],
                        "color": "#4B3A15"
                    },

                    {
                        "range": [70, 100],
                        "color": "#4A1E1E"
                    }

                ],

                "threshold": {

                    "line": {
                        "color": "#FFFFFF",
                        "width": 6
                    },

                    "thickness": 0.8,

                    "value": percent

                }

            }

        )
    )

    fig.update_layout(

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        font={
            "color": "white"
        },

        height=380,

        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        )

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )