library("ggplot2")
library("scales")
library("dplyr")
library("tidyverse")

args = commandArgs(trailingOnly=TRUE)
data = read.csv(args[1], header = TRUE)

summary(data)

p <- ggplot(data, aes(x=nframes, y=nfaults, color=alg))
p <- p + geom_line() + scale_y_continuous(labels = scales::comma)
p <- p + facet_wrap(~tlb_size)
ggsave(p, file=paste(args[1], "png", sep="."))

p <- data %>% filter(alg == "fifo")
p <- p %>% ggplot(mapping = aes(x = tlb_size))
p <- p + geom_line(aes(y = nfaults), colour = "darkorange")
p <- p + geom_line(aes(y = tlb_count), colour = "darkorchid")
p <- p + scale_y_continuous(labels = scales::comma)
p <- p + facet_wrap(~nframes)
ggsave(p, file=paste(args[1], "FIFO", "tlb-fault", "png", sep="."))

p <- ggplot(data, aes(x=nframes, y=io, color=alg))
p <- p + geom_line() + scale_y_continuous(labels = scales::comma)
p <- p + facet_wrap(~tlb_size)
ggsave(p, file=paste(args[1], "io", "png", sep="."))

p <- ggplot(data, aes(x=tlb_size, y=tlb_count, color=alg))
p <- p + geom_point() + scale_y_continuous(labels = scales::comma)
ggsave(p, file=paste(args[1], "tlb", "png", sep="."))

p <- ggplot(data, aes(x=tlb_size, y=nfaults, color=alg))
p <- p + geom_line() + scale_y_continuous(labels = scales::comma)
p <- p + facet_wrap(~nframes)
ggsave(p, file=paste(args[1], "io", "tlb", "png", sep="."))
