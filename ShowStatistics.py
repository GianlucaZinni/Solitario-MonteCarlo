from func.Statistics import fetch_data, plot_victory_by_strategy, plot_duration_by_strategy, plot_victory_percentage_by_strategy

df = fetch_data()
plot_victory_by_strategy(df)
plot_duration_by_strategy(df)
plot_victory_percentage_by_strategy(df)