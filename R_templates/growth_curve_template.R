# ============================================================
# Growth curve plotting template
# Purpose: Plot microbial growth curves from biological replicates
# Input format: wide-format data frame with time + replicate columns
# Output: mean ± SD growth curve
# ============================================================

library(tidyverse)
library(ggprism)

# ---- Example data ----
# Replace these example OD values with your own data.
# Keep the structure:
# time = sampling time
# StrainA_rep1, StrainA_rep2, StrainA_rep3
# StrainB_rep1, StrainB_rep2, StrainB_rep3

data <- data.frame(
  time = c(0, 24, 48, 72, 96, 120),

  StrainA_rep1 = c(0.10, 0.20, 0.35, 0.50, 0.68, 0.83),
  StrainA_rep2 = c(0.10, 0.21, 0.36, 0.51, 0.69, 0.84),
  StrainA_rep3 = c(0.10, 0.22, 0.37, 0.52, 0.70, 0.85),

  StrainB_rep1 = c(0.10, 0.24, 0.43, 0.69, 0.92, 1.08),
  StrainB_rep2 = c(0.10, 0.25, 0.44, 0.70, 0.95, 1.10),
  StrainB_rep3 = c(0.10, 0.26, 0.45, 0.71, 0.97, 1.12)
)

# ---- Convert from wide to long format ----

long_data <- data %>%
  pivot_longer(
    cols = -time,
    names_to = "sample",
    values_to = "OD"
  ) %>%
  mutate(
    strain = case_when(
      str_detect(sample, "StrainA") ~ "Strain A",
      str_detect(sample, "StrainB") ~ "Strain B",
      TRUE ~ "Unknown"
    ),
    strain = factor(strain, levels = c("Strain A", "Strain B"))
  )

# ---- Plot mean ± SD growth curve ----

p <- ggplot(long_data, aes(x = time, y = OD, color = strain, group = strain)) +

  stat_summary(
    fun = mean,
    geom = "line",
    linewidth = 1.5
  ) +

  stat_summary(
    fun = mean,
    geom = "point",
    size = 3
  ) +

  stat_summary(
    fun.data = mean_sdl,
    fun.args = list(mult = 1),
    geom = "errorbar",
    width = 5,
    linewidth = 0.7
  ) +

  scale_color_manual(
    values = c(
      "Strain A" = "#1f77b4",
      "Strain B" = "#e68626"
    )
  ) +

  scale_x_continuous(
    breaks = seq(0, 120, 24),
    limits = c(0, 120),
    expand = c(0, 0)
  ) +

  scale_y_continuous(
    limits = c(0, 1.5),
    breaks = seq(0, 1.5, 0.5),
    expand = c(0, 0)
  ) +

  labs(
    x = "Time (h)",
    y = expression(OD[600])
  ) +

  theme_prism(base_size = 18) +

  theme(
    panel.background = element_blank(),
    plot.background = element_blank(),
    axis.line = element_line(linewidth = 1.2),
    axis.ticks = element_line(linewidth = 1),
    axis.ticks.length = unit(0.15, "cm"),
    panel.grid = element_blank(),
    legend.title = element_blank(),
    legend.position = "top"
  )

print(p)

# ---- Save figure ----

ggsave(
  filename = "growth_curve_template.png",
  plot = p,
  width = 7,
  height = 5,
  dpi = 300
)
