# Initial exploratory analysis for bias in crowdsourced labels

#--------------
# Loading data #
#--------------#
path <- 'merged_conditions.csv'
df <- read.csv(path, colClasses = c('tweet_id' = 'character'))

#---------------
# Data cleaning #
#---------------#
dict <- c('no', 'some', 'lots')

# no-some-lots into 0-1-2 scale
df$anger <- match(df$anger, dict) - 1
df$happiness <- match(df$happiness, dict) - 1
df$worry <- match(df$worry, dict) - 1

# climate action into dummy for support vs everything else
df$climate_action_b <- ifelse(df$climate_action == 'support', 1, 0)

#--------------
# OLS analysis #
#--------------#
library(fixest);library(marginaleffects)

# emotion
m <- feols(worry ~ gender * ethnicity | tweet_id + worker_id, data = df, cluster = c('tweet_id', 'worker_id')); m
plot_cap(m, condition = c('ethnicity', 'gender'))

# climate support
m <- feols(climate_action_b ~ gender * ethnicity | tweet_id + worker_id, data = df, cluster = c('tweet_id', 'worker_id')); m
plot_cap(m, condition = c('ethnicity', 'gender'))
