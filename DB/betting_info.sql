
create table betting_info (

game_id varchar(50),

season varchar(50),

game_type varchar(50),

week int,

matchup varchar(50),

home_team varchar(50),

away_team varchar(50),

home_score int,
away_score int,
result int,
spread_line float(50),
spread_result varchar(50),
total int,
total_line float(50),
total_result varchar(50),
overtime int,
qb_matchup varchar(50),
home_qb_name varchar(50),
away_qb_name varchar(50),
coaching_matchup varchar(50),
home_coach varchar(50),
away_coach varchar(50),
conference varchar(50),
division varchar(50),
home_rest int,
away_rest int,
weekday varchar(50),
gametime varchar(50),
referee varchar(50),
stadium varchar(50),
roof varchar(50),
surface varchar(50),
temp int,
wind int,
weather varchar,
ATS_win int,
ATS_loss int,
ATS_push int,
over int,
under int,
push int,
div_game int,
home_moneyline int,
away_moneyline int,


	primary key(game_id)
)
