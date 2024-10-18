import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Configure Streamlit's layout and style
st.set_page_config(page_title="Dynamic Plotting Dashboard", layout="wide")
# Load custom CSS
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css("./style/style.css")

# Title of the app
st.title("Dynamic Plotting Dashboard")

# Upload CSV or Excel file
uploaded_file = st.file_uploader("Choose a CSV or Excel file", type=["csv", "xlsx"])

if uploaded_file is not None:
    # Load the data
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    # Show the dataframe
    st.write("### Data Preview:")
    st.dataframe(df)

    # Select the type of plot
    plot_type = st.selectbox("### Select Plot Type", [
        "Bar Chart",
        "Line Chart",
        "Scatter Plot",
        "Histogram",
        "Box Plot",
        "Pie Chart"
    ])

    # X-axis is needed only for certain plots
    x_axis = None
    if plot_type not in ["Pie Chart"]:
        x_axis = st.selectbox("### Select X-axis", df.columns)

    y_axes = []
    if plot_type in ["Bar Chart", "Line Chart", "Scatter Plot", "Histogram", "Box Plot"]:
        y_axes = st.multiselect("### Select Y-axes", df.columns)

    # For pie chart, allow multiple selections
    pie_variables = []
    if plot_type == "Pie Chart":
        pie_variables = st.multiselect("### Select Variables for Pie Chart", df.columns)

    if st.button("Generate Plot"):
        # Define a function for styling plots
        def set_style():
            plt.style.use('ggplot')  # Use a valid style
            plt.rcParams['axes.titlesize'] = 16
            plt.rcParams['axes.labelsize'] = 12
            plt.rcParams['xtick.labelsize'] = 10
            plt.rcParams['ytick.labelsize'] = 10
            plt.rcParams['legend.fontsize'] = 10
            plt.rcParams['figure.figsize'] = (12, 6)

        if plot_type == "Bar Chart":
            set_style()
            plt.figure()
            for y_axis in y_axes:
                df[y_axis].value_counts().plot(kind='bar', alpha=0.7, label=y_axis)
            plt.title(f'Bar Chart of {", ".join(y_axes)}', fontsize=18)
            plt.xlabel(x_axis, fontsize=12)
            plt.ylabel('Count', fontsize=12)
            plt.grid(True)
            plt.legend(title="Y-axes")
            st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
            st.pyplot(plt)
            st.markdown("</div>", unsafe_allow_html=True)

        elif plot_type == "Line Chart":
            set_style()
            plt.figure()
            for y_axis in y_axes:
                df[y_axis].value_counts().sort_index().plot(kind='line', label=y_axis)
            plt.title(f'Line Chart of {", ".join(y_axes)}', fontsize=18)
            plt.xlabel(x_axis, fontsize=12)
            plt.ylabel('Count', fontsize=12)
            plt.grid(True)
            plt.legend(title="Y-axes")
            st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
            st.pyplot(plt)
            st.markdown("</div>", unsafe_allow_html=True)

        elif plot_type == "Scatter Plot":
            set_style()
            plt.figure()
            for y_axis in y_axes:
                plt.scatter(df[x_axis], df[y_axis], alpha=0.7, label=y_axis)
            plt.title(f'Scatter Plot: {", ".join(y_axes)} vs {x_axis}', fontsize=18)
            plt.xlabel(x_axis, fontsize=12)
            plt.ylabel('Values', fontsize=12)
            plt.grid(True)
            plt.legend(title="Y-axes")
            st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
            st.pyplot(plt)
            st.markdown("</div>", unsafe_allow_html=True)

        elif plot_type == "Histogram":
            set_style()
            plt.figure()
            for y_axis in y_axes:
                df[y_axis].plot(kind='hist', bins=20, alpha=0.7, label=y_axis)
            plt.title(f'Histogram of {", ".join(y_axes)}', fontsize=18)
            plt.xlabel('Values', fontsize=12)
            plt.ylabel('Frequency', fontsize=12)
            plt.grid(True)
            plt.legend(title="Y-axes")
            st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
            st.pyplot(plt)
            st.markdown("</div>", unsafe_allow_html=True)

        elif plot_type == "Box Plot":
            set_style()
            plt.figure()
            for y_axis in y_axes:
                sns.boxplot(x=df[x_axis], y=df[y_axis], label=y_axis, palette='Set2', alpha=0.7)
            plt.title(f'Box Plot of {", ".join(y_axes)} vs {x_axis}', fontsize=18)
            plt.xlabel(x_axis, fontsize=12)
            plt.ylabel('Values', fontsize=12)
            plt.grid(True)
            plt.legend(title="Y-axes")
            st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
            st.pyplot(plt)
            st.markdown("</div>", unsafe_allow_html=True)

        elif plot_type == "Pie Chart":
            for variable in pie_variables:
                value_counts = df[variable].value_counts()
                fig = px.pie(
                    names=value_counts.index,
                    values=value_counts,
                    title=f'Pie Chart of {variable}',
                    hole=0.3,  # Optional: makes it a donut chart
                    color_discrete_sequence=px.colors.sequential.RdBu  # Better color palette
                )

                # Custom hover template
                fig.update_traces(
                    hovertemplate=f"{variable}: %{{label}}<br>Count: %{{value}}<extra></extra>"
                )

                # Update layout
                fig.update_layout(
                    legend_title_text=variable,
                    legend=dict(
                        font=dict(size=14, color="black", family="Arial")
                    ),
                    title_font_size=18,
                    title_x=0.5  # Center the title
                )
                
                # Centering the plotly chart
                st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
                st.plotly_chart(fig, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
