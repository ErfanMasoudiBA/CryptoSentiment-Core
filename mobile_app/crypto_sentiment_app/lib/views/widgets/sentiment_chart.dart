import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';

class SentimentChart extends StatelessWidget {
  final int positive;
  final int negative;
  final int neutral;

  const SentimentChart({
    super.key,
    required this.positive,
    required this.negative,
    required this.neutral,
  });

  @override
  Widget build(BuildContext context) {
    final total = positive + negative + neutral;

    if (total == 0) {
      return Card(
        margin: const EdgeInsets.all(16),
        child: Padding(
          padding: const EdgeInsets.all(32),
          child: Column(
            children: [
              const Icon(Icons.pie_chart_outline, size: 48, color: Colors.grey),
              const SizedBox(height: 16),
              const Text(
                'No data available',
                style: TextStyle(fontSize: 16, color: Colors.grey),
              ),
            ],
          ),
        ),
      );
    }

    return Card(
      margin: const EdgeInsets.all(16),
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Text(
              'Sentiment Distribution',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 16),
            SizedBox(
              height: 200,
              width: 200,
              child: PieChart(
                PieChartData(
                  sectionsSpace: 2,
                  centerSpaceRadius: 40,
                  sections: _buildPieChartSections(),
                ),
              ),
            ),
            const SizedBox(height: 16),
            _buildLegend(),
          ],
        ),
      ),
    );
  }

  List<PieChartSectionData> _buildPieChartSections() {
    final total = positive + negative + neutral;

    final sections = <PieChartSectionData>[];

    if (positive > 0) {
      sections.add(
        PieChartSectionData(
          color: Colors.green,
          value: positive.toDouble(),
          title: '${(positive / total * 100).toStringAsFixed(1)}%',
          radius: 50,
          titleStyle: const TextStyle(
            fontSize: 12,
            fontWeight: FontWeight.bold,
            color: Colors.white,
          ),
        ),
      );
    }

    if (negative > 0) {
      sections.add(
        PieChartSectionData(
          color: Colors.red,
          value: negative.toDouble(),
          title: '${(negative / total * 100).toStringAsFixed(1)}%',
          radius: 50,
          titleStyle: const TextStyle(
            fontSize: 12,
            fontWeight: FontWeight.bold,
            color: Colors.white,
          ),
        ),
      );
    }

    if (neutral > 0) {
      sections.add(
        PieChartSectionData(
          color: Colors.grey,
          value: neutral.toDouble(),
          title: '${(neutral / total * 100).toStringAsFixed(1)}%',
          radius: 50,
          titleStyle: const TextStyle(
            fontSize: 12,
            fontWeight: FontWeight.bold,
            color: Colors.white,
          ),
        ),
      );
    }

    return sections;
  }

  Widget _buildLegend() {
    final total = positive + negative + neutral;

    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
      children: [
        if (positive > 0)
          _legendItem('Positive', Colors.green, positive, total),
        if (negative > 0) _legendItem('Negative', Colors.red, negative, total),
        if (neutral > 0) _legendItem('Neutral', Colors.grey, neutral, total),
      ],
    );
  }

  Widget _legendItem(String label, Color color, int count, int total) {
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        Container(
          width: 12,
          height: 12,
          decoration: BoxDecoration(color: color, shape: BoxShape.circle),
        ),
        const SizedBox(width: 4),
        Text(
          '$label (${(count / total * 100).toStringAsFixed(1)}%)',
          style: const TextStyle(fontSize: 12, fontWeight: FontWeight.w500),
        ),
      ],
    );
  }
}
