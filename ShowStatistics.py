from func.Statistics import (fetch_data, plot_victory_by_strategy, plot_duration_by_strategy, 
                            plot_mean_moves_by_victory, plot_percentage_by_strategy_of_total_wins,
                            plot_scatter_duration_movements, plot_duration_histogram, plot_convergence_line)

df = fetch_data()
plot_convergence_line(df)
plot_mean_moves_by_victory(df)
plot_victory_by_strategy(df)
plot_duration_by_strategy(df)
plot_percentage_by_strategy_of_total_wins(df)
plot_scatter_duration_movements(df)
plot_duration_histogram(df)
