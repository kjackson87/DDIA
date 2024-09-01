import os
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from typing import List, Tuple, Dict
import json

class Visualizer:
    def __init__(self, store_directory: str):
        self.store_directory = store_directory
        self.segment_files = self._get_segment_files()
        self.colors = plt.cm.get_cmap('Set3').colors

    def _get_segment_files(self) -> List[str]:
        return sorted([f for f in os.listdir(self.store_directory) if f.endswith('.seg')])

    def _read_segment(self, segment_file: str) -> List[Tuple[str, int]]:
        entries = []
        with open(os.path.join(self.store_directory, segment_file), 'r') as f:
            for line in f:
                entry = json.loads(line)
                entries.append((entry['key'], len(line)))
        return entries

    def visualize(self):
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.set_ylim(0, len(self.segment_files))
        ax.set_xlim(0, 1000)  # Adjust this value based on your segment size
        ax.set_yticks(range(len(self.segment_files)))
        ax.set_yticklabels(self.segment_files)
        ax.set_xlabel('Segment size (bytes)')
        ax.set_title('Log-Structured Key-Value Store Visualization')

        for i, segment_file in enumerate(self.segment_files):
            entries = self._read_segment(segment_file)
            x_offset = 0
            for key, size in entries:
                color = self.colors[hash(key) % len(self.colors)]
                rect = Rectangle((x_offset, i), size, 0.8, facecolor=color, edgecolor='black', alpha=0.7)
                ax.add_patch(rect)
                if size > 50:  # Only add text for larger rectangles
                    ax.text(x_offset + size/2, i + 0.4, key, ha='center', va='center', rotation=90, fontsize=8)
                x_offset += size

        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    store_directory = "path/to/your/store/directory"  # Update this with the actual path
    visualizer = Visualizer(store_directory)
    visualizer.visualize()