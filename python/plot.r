library("ggplot2")
library("scales")

args = commandArgs(trailingOnly=TRUE)
data = read.csv(args[1], header = TRUE)

summary(data)

p <- ggplot(data, aes(x=nframes, y=nfaults, color=alg))
p <- p + geom_line() + scale_y_continuous()
ggsave(p, file=paste(args[1], "png", sep="."))

p <- ggplot(data, aes(x=nframes, y=io, color=alg))
p <- p + geom_line() + scale_y_continuous()
ggsave(p, file=paste(args[1], "io", "png", sep="."))
