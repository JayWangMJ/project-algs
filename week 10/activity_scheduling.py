# Activity scheduling problem using greedy and dp algorithm

def activity_scheduling_dp(activities):
    n = len(activities)
    activities = sorted(activities, key=lambda x: x[0])

    # Initialize
    dp = [0]*n
    dp[n-1] = 1

    # dp euqations
    # dp[i...n] = max{dp[i+1...n], 1+dp[p(i)...n]}
    for i in reversed(range(n-1)):
        # get the p(i): next acitivity that can be scheduled after i
        j = i+1
        while j < n and activities[j][0] < activities[i][1]:
            j += 1

        dp[i] = max(dp[i+1], 1+dp[j] if j < n else 0)

    print(dp)

    # revocer solution
    activities_sheduled = []
    i = 0
    while i < n-1:
        # i is not selected
        if dp[i] == dp[i+1]:
            i += 1
            continue

        j = i + 1
        while j < n and activities[j][0] < activities[i][1]:
            j += 1
        
        activities_sheduled.append(activities[i])
        i = j
    if activities[n-1][0] >= activities_sheduled[-1][1]:
        activities_sheduled.append(activities[n-1])

    activities_sheduled
    return activities_sheduled


def activity_scheduling_greedy(activies):
    activies = sorted(activies, key= lambda x: x[1])
    activies_scheduled = [activies[0]]
    last_f_time = activies[0][1]

    for (s_time, f_time) in activies[1:]:
        if s_time >= last_f_time:
            activies_scheduled.append((s_time, f_time))
            last_f_time = f_time

    return activies_scheduled

if __name__ == "__main__":
    s_times = [0, 1, 3, 3, 4, 5, 6, 8]
    f_times = [6, 4, 5, 8, 7, 9, 10, 11]
    activities = list(zip(s_times, f_times))
    activities_scheduled_dp = activity_scheduling_dp(activities)
    activities_scheduled_greedy = activity_scheduling_greedy(activities)
    print(activities_scheduled_dp)
    print(activities_scheduled_greedy)