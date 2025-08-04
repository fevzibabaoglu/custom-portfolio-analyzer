# Custom Portfolio Analyzer

A Python tool to model, back-test, and compare the performance of custom investment portfolios based on historical data. It visualizes the profit-over-time for different portfolio configurations across specified date ranges.


## How It Works

The tool operates based on two main input files:

1.  **An asset data CSV**: This file acts as the database for your assets (e.g., funds, stocks). It stores the name, a unique code, and the historical prices for each asset.

2.  **A portfolio configuration JSON**: This file defines the analysis scenarios. Here, you specify one or more comparisons scenarios, each containing the portfolios to be analyzed and compared, and the date ranges for back-testing.

The script reads these files, calculates the performance of each portfolio for each date range using a **Static Allocation Performance Index**, and then generates a plot for each scenario, showing the profit ratio over time.


### Static Allocation Performance Index

The core of the analysis is the Static Allocation Performance Index. This formula calculates the value of a portfolio at a given point in time, assuming a fixed (static) allocation of assets. It measures the weighted average performance of the individual assets relative to their starting prices.

$$
\text{SAPI} = \frac{\sum_{i} \left( w_i \cdot \frac{P_{i}}{P_{i0}} \right)}{\sum_{i} \left( w_i \cdot \frac{1}{P_{i0}} \right)}
$$

Where:

*   **`SAPI`** is the Static Allocation Performance Index value.
*   $w_i$ is the weight (allocation) of asset *i* in terms of money.
*   $P_{i0}$ is the initial price of asset *i* at the beginning of the date range.
*   $P_{i}$ is the price of asset *i* on each subsequent day within the analysis period.
*   $\sum_{i}$ denotes the sum over all assets (*i*) in the portfolio.


## File Structure & Configuration

### Asset Data

This is a simple CSV file that lists each asset and its historical price data. See **[asset_data.csv](./data_example/asset_data.csv)** for an example of the required format.

The data for this file needs to be gathered from an external source. My another project, **[TEFAS Fund Data Exporter](https://github.com/fevzibabaoglu/tefas-data-exporter)**, can be used to collect the historical price points for each fund you wish to include in your analysis.

### Portfolio Configuration

This file is a list of comparison scenarios. Each scenario defines the portfolios you want to compare and the time periods for the analysis. For a detailed example of the required structure, please see the **[portfolio_comparison_config.json](./data_example/portfolio_comparison_config.json)** file.

**Note:** The `set_default` field is optional and defaults to `false`. It should be explicitly set to `true` for only one portfolio within a scenario. When provided, it marks that portfolio as the baseline, and all comparisons will be made relative to it. If omitted, no baseline portfolio is assumed.


## How to Run

### Dependencies

Ensure you have the required Python libraries.

```shell
pip install -r requirements.txt
```


### Executing the Script

Run the main script from your terminal. The script will generate and display a chart for each analysis defined in your configuration files.

```shell
python src/main.py
```


### Command-Line Arguments

You can customize the file paths and date display format using the following arguments:

*   `--asset-data-path`: Path to your asset data CSV file.
    *   Default: `data/asset_data.csv`
*   `--config-path`: Path to your portfolio configuration JSON file.
    *   Default: `data/portfolio_comparison_config.json`
*   `--date-format`: The format for displaying dates on the chart axes (must be a valid Python `strftime` format).
    *   Default: `%d.%m.%Y` (Keep as default for `TEFAS Fund Data Exporter` compatibility)

*Example with arguments:*
```shell
python src/main.py --asset-data-path "path/to/my_assets.csv" --config-path "path/to/my_config.json" --date-format "%Y-%m-%d"
```


***

## License

This project is licensed under the terms of the **GNU Lesser General Public License v3.0**.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Lesser General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.

This program is distributed in the hope that it will be useful, but **WITHOUT ANY WARRANTY**; without even the implied warranty of **MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE**. See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU General Public License and the GNU Lesser General Public License along with this program. If not, see <https://www.gnu.org/licenses/>.

The full text of the licenses can be found in the root of this project:

*   **[COPYING](./COPYING)** (The GNU General Public License)
*   **[COPYING.LESSER](./COPYING.LESSER)** (The GNU Lesser General Public License)
