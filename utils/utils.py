
def limit_table(exp, obs):
    file = open('limits.yaml', 'w')
    for i in range(len(exp.x)):
        file.write(
            '%.2f: [%.6f, %.6f, %.6f, %.6f, %.6f, %.6f]\n' % (
                exp.x[i], exp.y[i],
                exp.bands[1][1][i] - exp.y[i], exp.bands[1][0][i] - exp.y[i],
                exp.bands[0][1][i] - exp.y[i], exp.bands[0][0][i] - exp.y[i],
                obs.y[i]
            )
        )

