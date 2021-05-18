from typing import List, Optional


class SegmentsSplitter:
    def __init__(self, seconds_per_segment: float, additional_segments_seconds_delay=None):
        if additional_segments_seconds_delay is None:
            additional_segments_seconds_delay = []
        self.seconds_per_segment = seconds_per_segment
        self.additional_segments_seconds_delay = \
            [0] + ([] if additional_segments_seconds_delay is None else additional_segments_seconds_delay)

    def split(self, track: any, sample_rate: int) -> Optional[List[any]]:
        samples_per_segment = sample_rate * self.seconds_per_segment
        if len(track) // samples_per_segment == 0:
            return None
        segments = []
        for delay in self.additional_segments_seconds_delay:
            delay_in_samples = sample_rate * delay
            number_of_segments = (len(track) - delay_in_samples) // samples_per_segment
            for i in range(number_of_segments):
                segment = track[delay_in_samples + i * samples_per_segment:
                                delay_in_samples + i * samples_per_segment + samples_per_segment]
                segments.append(segment)
        return segments
