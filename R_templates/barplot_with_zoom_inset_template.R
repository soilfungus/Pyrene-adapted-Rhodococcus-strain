# ============================================================
# Bar Plot with Zoomed Inset Template
#
# Author:
# Gabriela Calcáneo-Hernández
#
# Purpose:
# Plot grouped biological replicate data as mean ± SD,
# show individual points, and add a zoomed inset for one condition.
#
# Dependencies:
# tidyverse
# ggprism
# cowplot
#
# ============================================================

library(tidyverse)
library(ggprism)
library(cowplot)

# ---- Example data ----

data <- data.frame(
  group = c(
    rep("Group_A", 6),
    rep("Group_B", 6)
  ),

  condition = c(
    rep("Low dose", 3),
    rep("High dose", 3),
    rep("Low dose", 3),
    rep("High dose", 3)
  ),

  response = c(
    10, 12, 11,
    1.0, 1.2, 0.9,
    80, 85, 78,
    2.5, 2.8, 2.3
  )
)

data$group <- factor(data$group, levels = c("Group_A", "Group_B"))

data$condition <- factor(data$condition, levels = c("Low dose", "High dose"))

# ---- Main plot ----

p_main <- ggplot(
  data,
  aes(
    x = condition,
    y = response,
    fill = group
  )
) +

  stat_summary(
    fun = mean,
    geom = "bar",
    position = position_dodge(width = 0.7),
    width = 0.6,
    color = "black"
  ) +

  stat_summary(
    fun.data = mean_sdl,
    fun.args = list(mult = 1),
    geom = "errorbar",
    position = position_dodge(width = 0.7),
    width = 0.2,
    linewidth = 0.8
  ) +

  geom_point(
    position = position_jitterdodge(
      jitter.width = 0.08,
      dodge.width = 0.7
    ),
    size = 2.5,
    shape = 21,
    color = "black"
  ) +

  scale_fill_manual(
    values = c(
      "Group_A" = "grey80",
      "Group_B" = "grey35"
    )
  ) +

  scale_y_continuous(
    limits = c(0, 100),
    breaks = seq(0, 100, 20),
    expand = c(0, 0)
  ) +

  labs(
    x = "Condition",
    y = "Response (%)"
  ) +

  theme_prism(base_size = 14) +

  theme(
    legend.position = "top",
    legend.title = element_blank(),
    axis.title = element_text(face = "bold"),
    axis.text = element_text(face = "bold"),
    axis.line = element_line(linewidth = 1.2),
    axis.ticks = element_line(linewidth = 1.2),
    axis.ticks.length = unit(0.25, "cm")
  )

# ---- Zoomed inset plot ----
# Choose one condition to highlight

zoom_data <- data %>%
  filter(condition == "High dose")

p_zoom <- ggplot(
  zoom_data,
  aes(
    x = group,
    y = response,
    fill = group
  )
) +

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
    width = 0.2
  ) +

  geom_jitter(
    width = 0.05,
    size = 2,
    shape = 21,
    color = "black"
  ) +

  scale_fill_manual(
    values = c(
      "Group_A" = "grey80",
      "Group_B" = "grey35"
    )
  ) +

  scale_y_continuous(
    limits = c(0, 4),
    breaks = seq(0, 4, 1),
    expand = c(0, 0)
  ) +

  labs(
    x = NULL,
    y = NULL
  ) +

  theme_prism(base_size = 8) +

  theme(
    legend.position = "none",
    axis.text = element_text(face = "bold", size = 7),
    axis.line = element_line(linewidth = 0.8),
    axis.ticks = element_line(linewidth = 0.8)
  )

# ---- Combine main plot and inset ----

final_plot <- ggdraw() +
  draw_plot(p_main) +
  draw_plot(
    p_zoom,
    x = 0.57,
    y = 0.43,
    width = 0.33,
    height = 0.33
  )

print(final_plot)

# ---- Save figure ----

ggsave(
  filename = "barplot_with_zoom_inset_template.png",
  plot = final_plot,
  width = 7,
  height = 5,
  dpi = 300
)
