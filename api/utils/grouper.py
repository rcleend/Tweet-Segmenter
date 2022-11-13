from nltk.stem.porter import PorterStemmer

class Grouper:
    def __init__(self):
        self.stemmer = PorterStemmer()

    def group_by_stem_and_sort_by_freq(self, segments):
        grouped_segments = []
        grouped_segments_len = 0

        for segment in segments:
            # Create stem to group by stem instead
            stem = self.stemmer.stem(segment)

            # Add first segment to grouped segments list so it isn't empty
            if grouped_segments_len == 0:
                grouped_segments.append((segment, stem, 1))
                grouped_segments_len += 1
                continue

            for i, (grouped_segment, grouped_stem, freq) in enumerate(grouped_segments):
                # Save index of segment with at least one frequency higher than current segment
                if i == 0 or higher_freq > freq:
                    higher_freq_index = i
                    higher_freq = freq

                # Update frequency grouped segment when found
                if grouped_stem == stem:
                    freq += 1
                    entry = (grouped_segment, grouped_stem, freq)

                    # Sort grouped segment to higher freq
                    if higher_freq <= freq:
                        grouped_segments.pop(i)
                        grouped_segments.insert(higher_freq_index, entry)
                    else:
                        grouped_segments[i] = entry

                    break

                # Append grouped segments list if no equal segment has been found
                elif i == grouped_segments_len - 1:
                    grouped_segments.append((segment, stem, 1))
                    grouped_segments_len += 1

        return grouped_segments
