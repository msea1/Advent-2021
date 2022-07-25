def sonar_sweep(puzzle_input: list[str | int]) -> int:
    # https://adventofcode.com/2021/day/1
    increases = 0
    for i in range(1, len(puzzle_input)):
        if int(puzzle_input[i]) > int(puzzle_input[i - 1]):
            increases += 1
    return increases


def sonar_sweep_window(window_size: int, puzzle_input: list[str | int]) -> int:
    # https://adventofcode.com/2021/day/1
    increases = 0

    # initialize the window with the first n inputs
    window_a = sum(int(x) for x in puzzle_input[:window_size])

    for i in range(window_size, len(puzzle_input)):
        # add the latest value and drop the earliest value
        window_b = window_a + int(puzzle_input[i]) - int(puzzle_input[i-window_size])
        if window_b > window_a:
            increases += 1
        window_a = window_b
    return increases


def steer(instructions: list[str]) -> int:
    # https://adventofcode.com/2021/day/2
    position, depth = 0, 0
    for line in instructions:
        if not line:
            continue
        line = line.strip()
        direction, amount = line.split(" ")
        amount = int(amount)
        if direction == "forward":
            position += amount
        elif direction == "down":
            depth += amount
        elif direction == "up":
            depth = max(0, depth-amount)
    return position * depth


def steer_aim(instructions: list[str]) -> int:
    # https://adventofcode.com/2021/day/2
    position, depth, aim = 0, 0, 0
    for line in instructions:
        if not line:
            continue
        line = line.strip()
        direction, amount = line.split(" ")
        amount = int(amount)
        if direction == "forward":
            position += amount
            depth = max(0, depth+aim*amount)
        elif direction == "down":
            aim += amount
        elif direction == "up":
            aim -= amount
    return position * depth


def _evaluate_diagnostic_report(report: list[str], tie_marker: str = "1") -> str:
    notches = []
    # TODO: might be a more compact struct to use here or make use of bit math?
    for diag in report:
        for i, toggle in enumerate(reversed(diag)):
            t = int(toggle)
            if len(notches) <= i:
                notches.append(t)
            else:
                notches[i] += t
    gamma = ""
    border = len(report)/2
    for n in notches:
        gamma += "1" if n > border else "0" if n < border else tie_marker
    return gamma[::-1]


def determine_power_consumption(diagnostics: list[str]) -> int:
    # https://adventofcode.com/2021/day/3
    gamma_str = _evaluate_diagnostic_report(diagnostics)
    gamma_x = int(gamma_str, 2)
    all_ones = 2**len(gamma_str)-1
    ep_x = gamma_x ^ all_ones
    return gamma_x*ep_x


def _weed_out_unmatched_entries(entries: list[str], bit_num: int, find_most: bool) -> str:
    if not entries:  # weeded everyone out, should not be possible
        return "0"  # TODO assumption on return here
    if len(entries) == 1:  # weeded out all but 1
        return entries[0]
    if bit_num >= len(entries[0]):  # reached end of pattern and still have multiple answers left
        return "0"  # TODO assumption on return here
    # don't use tie_marker here because we will invert it if not finding most
    pattern = _evaluate_diagnostic_report(entries).zfill(len(entries[0]))
    if not find_most:
        _g = int(pattern, 2)
        all_ones = 2**len(pattern)-1
        pattern = format(_g ^ all_ones, 'b').zfill(len(entries[0]))
    wheat = [
        entry for entry in entries if entry[bit_num] == pattern[bit_num]
    ]
    return _weed_out_unmatched_entries(wheat, bit_num + 1, find_most)


def get_life_support_rating(diagnostics: list[str]) -> int:
    # https://adventofcode.com/2021/day/3#part2
    if not diagnostics:
        return 0
    oxy_gen_rating = _weed_out_unmatched_entries(diagnostics, 0, True)
    co2_scrubber_rating = _weed_out_unmatched_entries(diagnostics, 0, False)
    return int(oxy_gen_rating, 2) * int(co2_scrubber_rating, 2)
