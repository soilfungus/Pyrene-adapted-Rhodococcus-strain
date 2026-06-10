# ============================================================
# Time-Course Bar Plot with Statistical Comparisons
#
# Author:
# Gabriela Calcáneo-Hernández
#
# Purpose:
# Compare two experimental groups across multiple time points using mean ± SD and Student's t-tests.
# 
# Dependencies:
# tidyverse
# ggpubr
# rstatix
#
# Citation:
# Wickham et al. (2019) tidyverse
# Kassambara A. ggpubr
# Kassambara A. rstatix
# ============================================================

library(tidyverse)
library(ggpubr)
library(rstatix)

# ---- Example data ----
# Replace with your own measurements

data <- data.frame(
  time = c(10, 20, 30, 40, 50, 60),

  GroupA_rep1 = c(3, 8, 15, 22, 30, 38),
  GroupA_rep2 = c(4, 9, 14, 25, 31, 40),
  GroupA_rep3 = c(3, 7, 16, 23, 29, 39),

  GroupB_rep1 = c(5, 14, 28, 40, 48, 55),
  GroupB_rep2 = c(6, 16, 30, 42, 50, 58),
  GroupB_rep3 = c(5, 15, 29, 41, 47, 56)
)

# ---- Convert to long format ----

long <- data %>%
  pivot_longer(
    -time,
    names_to = "sample",
    values_to = "value"
  ) %>%
  mutate(
    group = case_when(
      str_detect(sample, "GroupA") ~ "Group A",
      str_detect(sample, "GroupB") ~ "Group B"
    ),
    group = factor(group,
                   levels = c("Group A", "Group B"))
  )

# ---- Statistical comparison ----

stat.test <- long %>%
  group_by(time) %>%
  t_test(value ~ group) %>%
  add_significance()

# Automatic label placement
max_y <- max(long$value)

stat.test <- stat.test %>%
  mutate(
    xmin = as.character(time),
    xmax = as.character(time),
    y.position = seq(
      max_y * 1.10,
      max_y * 1.30,
      length.out = n()
    )
  )

# ---- Plot ----

p <- ggplot(
  long,
  aes(
    x = factor(time),
    y = value,
    fill = group
  )
) +

  stat_summary(
    fun = mean,
    geom = "bar",
    position = position_dodge(0.7),
    width = 0.6,
    color = "black"
  ) +

  stat_summary(
    fun.data = mean_sdl,
    fun.args = list(mult = 1),
    geom = "errorbar",
    position = position_dodge(0.7),
    width = 0.2,
    linewidth = 0.7
  ) +

  stat_pvalue_manual(
    stat.test,
    label = "p.signif",
    xmin = "xmin",
    xmax = "xmax",
    y.position = "y.position",
    tip.length = 0
  ) +

  scale_fill_manual(
    values = c(
      "Group A" = "grey80",
      "Group B" = "grey35"
    )
  ) +

  labs(
    x = "Time",
    y = "Response variable"
  ) +

  theme_classic(base_size = 14) +

  theme(
    axis.title = element_text(face = "bold"),
    axis.text = element_text(face = "bold"),
    axis.line = element_line(linewidth = 1.2),
    axis.ticks = element_line(linewidth = 1.2),
    legend.title = element_blank(),
    legend.position = "top"
  )

print(p)

# ---- Save figure ----

ggsave(
  "timecourse_barplot_statistics_template.png",
  p,
  width = 7,
  height = 5,
  dpi = 300
)
