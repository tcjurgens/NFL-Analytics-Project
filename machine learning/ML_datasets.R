library(tidyverse)
library(nflfastr)
library(glue)

pbp <- load_pbp(2011:2021)

games <- pbp %>% 
  select(game_id, season, week, home_team, away_team, posteam, defteam, play_type, epa, home_score, away_score, total, result)

load_sharpe_data <- function(file_name) {
  url <- glue("https://raw.githubusercontent.com/nflverse/nfldata/master/data/{file_name}.csv")
  suppressWarnings({ df <- read_csv(url, col_types = cols()) })
  return(df)
}
scheduled_games <- load_sharpe_data("games") %>% filter(season %in% c(2011:2021)) %>%
  select(game_id, spread_line, total_line)

for(row in 1:nrow(scheduled_games)) {
  scheduled_games[row,'spread_line'] <- (scheduled_games[row,'spread_line'])*-1
}
for(row in 1:nrow(games)) {
  games[row,'result'] <- (games[row,'result'])*-1
}

ML_data <- full_join(scheduled_games, games, by = "game_id")

# Offense EPA
offensive_epa_data <- ML_data %>%
  filter(!is.na(epa), !is.na(posteam), play_type == "pass" | play_type == "run" ) %>%
  group_by(game_id, season, week, posteam, home_team) %>%
  summarize(off_epa = mean(epa),
            off_pass_epa = mean(epa[play_type == "pass"]),
            off_rush_epa = mean(epa[play_type == "run"]),
            .groups = "drop")
  # Defensive EPA
defensive_epa_data <- ML_data %>%
  filter(!is.na(epa), !is.na(posteam), play_type == "pass" | play_type == "run" ) %>%
  group_by(game_id, season, week, defteam, away_team) %>%
  summarize(def_epa = mean(epa),
            def_pass_epa = mean(epa[play_type == "pass"]),
            def_rush_epa = mean(epa[play_type == "run"]),
            .groups = "drop")

# join the two datasets
epa_data <- left_join(offensive_epa_data, defensive_epa_data, by = c("game_id", "season", "week", "posteam" = "defteam")) %>%
  mutate(defteam = ifelse(posteam == home_team, away_team, home_team)) %>%
  select(game_id, season, week, home_team, away_team, posteam, defteam,
         off_epa, off_pass_epa, off_rush_epa,
         def_epa, def_pass_epa, def_rush_epa)

spread_data <- ML_data %>% 
  select(game_id, total_line, spread_line, home_score, away_score, result, total)

epa_data_full <- full_join(spread_data, epa_data, by = "game_id")
epa_data_full <- epa_data_full %>% distinct() 


write.csv(epa_data_full,'/Users/tcjurgens/Documents/Data_Final_Project/NFL-Analytics-Project/machine learning/ML_epa_data.csv')

            



