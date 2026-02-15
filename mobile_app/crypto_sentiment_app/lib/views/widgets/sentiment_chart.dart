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
      return Padding(
        padding: const EdgeInsets.all(32),
        child: Column(
          children: [
            Icon(
              Icons.pie_chart_outline,
              size: 48,
              color: Colors.grey.shade600,
            ),
            const SizedBox(height: 16),
            Text(
              'No data available',
              style: TextStyle(
                fontSize: 16,
                color: Colors.grey.shade400,
              ),
            ),
          ],
        ),
      );
    }

    return Padding(
      padding: const EdgeInsets.all(20),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          const Text(
            'Market Sentiment',
            style: TextStyle(
              fontSize: 20,
              fontWeight: FontWeight.bold,
              color: Colors.white,
            ),
          ),
          const SizedBox(height: 20),
          SizedBox(
            height: 220,
            width: 220,
            child: PieChart(
              PieChartData(
                sectionsSpace: 3,
                centerSpaceRadius: 50,
                sections: _buildPieChartSections(),
              ),
            ),
          ),
          const SizedBox(height: 20),
          _buildLegend(),
        ],
      ),
    );
  }

  List<PieChartSectionData> _buildPieChartSections() {
    final total = positive + negative + neutral;

    final sections = <PieChartSectionData>[];

    if (positive > 0) {
      sections.add(
        PieChartSectionData(
          color: Colors.green.shade500,
          value: positive.toDouble(),
          title: '${(positive / total * 100).toStringAsFixed(1)}%',
          radius: 60,
          titleStyle: const TextStyle(
            fontSize: 13,
            fontWeight: FontWeight.bold,
            color: Colors.white,
          ),
        ),
      );
    }

    if (negative > 0) {
      sections.add(
        PieChartSectionData(
          color: Colors.red.shade500,
          value: negative.toDouble(),
          title: '${(negative / total * 100).toStringAsFixed(1)}%',
          radius: 60,
          titleStyle: const TextStyle(
            fontSize: 13,
            fontWeight: FontWeight.bold,
            color: Colors.white,
          ),
        ),
      );
    }

    if (neutral > 0) {
      sections.add(
        PieChartSectionData(
          color: Colors.grey.shade500,
          value: neutral.toDouble(),
          title: '${(neutral / total * 100).toStringAsFixed(1)}%',
          radius: 60,
          titleStyle: const TextStyle(
            fontSize: 13,
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
          _legendItem('Positive', Colors.green.shade500, positive, total),
        if (negative > 0)
          _legendItem('Negative', Colors.red.shade500, negative, total),
        if (neutral > 0)
          _legendItem('Neutral', Colors.grey.shade500, neutral, total),
      ],
    );
  }

  Widget _legendItem(String label, Color color, int count, int total) {
    return Column(
      children: [
        Container(
          width: 16,
          height: 16,
          decoration: BoxDecoration(
            color: color,
            shape: BoxShape.circle,
          ),
        ),
        const SizedBox(height: 4),
        Text(
          label,
          style: TextStyle(
            fontSize: 12,
            fontWeight: FontWeight.w600,
            color: Colors.grey.shade300,
          ),
        ),
        Text(
          '${(count / total * 100).toStringAsFixed(1)}%',
          style: TextStyle(
            fontSize: 14,
            fontWeight: FontWeight.bold,
            color: color,
          ),
        ),
      ],
    );
  }
}
