import matplotlib.pyplot as plt

from environment import eNBs

# Testing eNB class


# Use matplotlib to plot the received power of the base station
# as a function of distance from the base station


x = [i for i in range(1, 50000)]

# Add y-axis labels at increments of 5
# add guidelines at increments of 5
plt.yticks([i for i in range(-110, 0, 5)])
for i in range(-110, 0, 5):
    plt.axhline(y=i, color='lightgrey', linestyle='-')


def get_line_color(bs_type):
    if bs_type == "lte":
        return "orange"
    elif bs_type == "nr":
        return "deepskyblue"


for e in eNBs:
    plt.plot(x, [e.calc_RSS(a) for a in x], label=e.get_type() + str(e.get_id()), markersize=1,
             color=get_line_color(e.get_type()))

# Set a min limit of -80 on
plt.ylim(-100, -30)
plt.xlabel("Distance from eNB(units not yet defined)")
plt.ylabel("Estimated RSS (dB)")
plt.legend()
plt.show()
