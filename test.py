from pv_sizing.app_layout.dashboard import interactive_plot
from pv_sizing.app_layout.applayout import app

interactive_plot()

if __name__ == "__main__":
    app.run_server(debug=True)

