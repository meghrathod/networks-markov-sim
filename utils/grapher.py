from matplotlib import pyplot as plt

import eNB_environments


def graph_rsrp(eNBs):
    """This function plots the received signal strength as a
    function of distance from the base station"""
    x = list(range(1, 50000))

    # Add y-axis labels at increments of 5
    # add guidelines at increments of 5
    plt.yticks(list(range(-300, 0, 5)))
    for i in range(-110, 0, 5):
        plt.axhline(y=i, color="lightgrey", linestyle="-")

    def get_line_color(bs_type):
        if bs_type == "lte":
            return "orange"
        if bs_type == "nr":
            return "deepskyblue"

    for e in eNBs:
        plt.plot(
            x,
            [e.calc_RSRP(a) for a in x],
            label=e.get_type() + str(e.get_id()),
            markersize=1,
            color=get_line_color(e.get_type()),
        )

    plt.ylim(-110, 0)
    plt.xlabel("Distance from eNB")
    plt.ylabel("Estimated RSRP (dBm)")
    plt.legend()
    plt.show()


graph_rsrp(eNB_environments.eNBs_mix1)
