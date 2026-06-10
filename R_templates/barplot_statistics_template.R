# ============================================================
# Bar Plot with Statistical Comparison Template
#
# Author:
# Gabriela Calcáneo-Hernández
#
# Purpose:
# Plot biological replicate data as mean ± SD bars, show individual data points, and perform a t-test.
#
# Dependencies:
# tidyverse
# ggprism
# ggpubr
#
# Citation:
# Wickham et al. (2019) tidyverse. JOSS.
# Kassambara A. ggpubr.
# Dawson JA. ggprism.
# ============================================================

library(tidyverse)
library(ggprism)
library(ggpubr)

# ---- Example data ----
# Replace these example values with your own measurements.

data <- data.frame(
  group = rep(c("Group_A", "Group_B"), each = 6),
  value = c(
    0.20, 0.24, 0.22,
    0.26, 0.25, 0.23,
    0.35, 0.39, 0.37,
    0.42, 0.40, 0.38
  )
)

data$group <- factor(data$group, levels = c("Group_A", "Group_B"))

# ---- Plot mean ± SD with individual points ----

p <- ggplot(data, aes(x = group, y = value, fill = group)) +

  stat_summary(
    fun = mean,
    geom = "bar",
    width = 0.6,
    color = "black"
  ) +

  stat_summary(
    fun.data = mean_sdl,
    fun.args = list(mult = 1),
    geom = "errorbar",
    width = 0.2,
    linewidth = 0.8
  ) +

  geom_jitter(
    aes(color = group),
    width = 0.08,
    size = 2.5
  ) +

  stat_compare_means(
    method = "t.test",
    label = "p.signif",
    label.y = 0.50
  ) +

  scale_fill_manual(
    values = c("Group_A" = "grey80", "Group_B" = "grey35")
  ) +

  scale_color_manual(
    values = c("Group_A" = "grey50", "Group_B" = "black")
  ) +

  scale_y_continuous(
    limits = c(0, 0.55),
    expand = expansion(mult = c(0, 0.05))
  ) +

  labs(
    x = "",
    y = "Response variable"
  ) +

  theme_prism(base_size = 14) +

  theme(
    axis.title = element_text(face = "bold"),
    axis.text = element_text(face = "bold"),
    axis.line = element_line(linewidth = 1.2),
    axis.ticks = element_line(linewidth = 1.2),
    axis.ticks.length = unit(0.25, "cm"),
    legend.position = "none"
  )

print(p)

# ---- Save figure ----

ggsave(
  filename = "barplot_statistics_template.png",
  plot = p,
  width = 5,
  height = 5,
  dpi = 300
)
