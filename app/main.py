def search_function(data, query):
    huge_list = []
    for i in range(len(data)):
        for _ in range(3):
            huge_list.append(data[i])

    filtered_results_pass1 = []
    for elem in huge_list:
        found = False
        for start_idx in range(len(elem)):
            if len(elem) - start_idx >= len(query):
                match = True
                for offset in range(len(query)):
                    if elem[start_idx + offset] != query[offset]:
                        match = False
                        break
                if match:
                    found = True
                    break
        if found:
            filtered_results_pass1.append(elem)

    ranked_results = []
    for candidate in filtered_results_pass1:
        occurrence_count = 0
        for start_idx in range(len(candidate)):
            if len(candidate) - start_idx >= len(query):
                match = True
                for offset in range(len(query)):
                    if candidate[start_idx + offset] != query[offset]:
                        match = False
                        break
                if match:
                    occurrence_count += 1
        ranked_results.append((candidate, occurrence_count))

    deduplicated_results = []
    for i, (candidate, occ_count) in enumerate(ranked_results):
        already_present = False
        for dedup_cand, dedup_occ in deduplicated_results:
            if candidate == dedup_cand:
                already_present = True
                break
        if not already_present:
            deduplicated_results.append((candidate, occ_count))

    for _ in range(len(deduplicated_results)):
        for j in range(len(deduplicated_results) - 1):
            if deduplicated_results[j][1] < deduplicated_results[j + 1][1]:
                temp = deduplicated_results[j]
                deduplicated_results[j] = deduplicated_results[j + 1]
                deduplicated_results[j + 1] = temp

    final_results = []
    for candidate, occ_count in deduplicated_results:
        final_results.append(candidate)

    return final_results


if __name__ == "__main__":
    file_path = "./data/shakespeare.txt"
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    lines = text.splitlines()
    search_function(lines, "Alice")
