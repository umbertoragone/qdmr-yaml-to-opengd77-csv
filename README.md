# QDMR .yaml to OpenGD77 .csv Converter

This python script converts data from a GD-77 YAML configuration file generated by [qdmr](https://github.com/hmatuschek/qdmr) into four separate CSV files compatible with the [OpenGD77 CPS](https://www.opengd77.com).

This conversion simplifies managing a single codeplug for multiple DMR radios, such as a Radioddity GD-77 and a Retevis RT-3S. Since qdmr does not yet support the RT-3S with the OpenGD77 firmware, I manage my codeplug in qdmr on a Linux system, then write it to my GD-77 with OpenGD77 firmware. This Python script converts the YAML codeplug from qdmr into four CSV files. I then use the OpenGD77 CPS on a Windows PC or VM (since it does not work on Linux) to write the codeplug to the RT-3S radio.

## Getting Started

### Prerequisites

Ensure you have Python installed on your system. This project requires Python 3.6 or higher.

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/umbertoragone/qdmr_yaml_to_opengd77_csv.git
   cd qdmr_yaml_to_opengd77_csv
   ```

2. Install the required Python packages:

   ```bash
   pip install pyyaml
   ```

### Usage

1. Place your `GD-77.yaml` file in the parent directory of your project folder.
2. Run the Python script to generate the CSV files:

   ```bash
   python qdmr_yaml_to_opengd77_csv.py
   ```

### File Structure

- `qdmr_yaml_to_opengd77_csv.py`: Main script to convert YAML to CSV.
- `GD-77.yaml`: Input YAML file containing the configuration data (should be placed in the parent directory).
- `Channels.csv`: Output CSV file for channels.
- `Contacts.csv`: Output CSV file for contacts.
- `TG_Lists.csv`: Outputs CSV file for group lists (TG lists).
- `Zones.csv`: Output CSV file for zones.

### Example

Ensure the following directory structure for the script to locate the YAML file correctly:

```
/path/to/parent/directory/
├── GD-77.yaml
└── OpenGD77 CSV/
  ├── qdmr_yaml_to_opengd77_csv.py
  ├── Channels.csv
  ├── Contacts.csv
  ├── TG_Lists.csv
  └── Zones.csv
```

## Contributing

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes.
4. Push to the branch.
5. Create a new Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thank you to the contributors of the PyYAML library.
- Special thanks to the OpenGD-77 community for their support and resources.

---

If you encounter any issues or have suggestions for improvement, please feel free to open an issue or submit a pull request.
