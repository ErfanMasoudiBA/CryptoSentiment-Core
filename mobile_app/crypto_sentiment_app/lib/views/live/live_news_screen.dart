import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:fl_chart/fl_chart.dart';
import '../../controllers/live_news_controller.dart';
import '../../models/live_news_model.dart';

class LiveNewsScreen extends StatelessWidget {
  final LiveNewsController controller = Get.put(LiveNewsController());

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Row(
          children: [
            Icon(Icons.radio, color: Colors.red),
            SizedBox(width: 8),
            Text('Live Market Pulse'),
          ],
        ),
        actions: [
          IconButton(
            icon: Icon(Icons.calendar_today),
            onPressed: () {
              _showDateRangePicker(context);
            },
          ),
          IconButton(
            icon: Obx(
              () => controller.isSyncing.isTrue
                  ? CircularProgressIndicator(strokeWidth: 2)
                  : Icon(Icons.refresh),
            ),
            onPressed: () {
              controller.fetchLiveNews();
            },
          ),
        ],
      ),
      body: Column(
        children: [
          // Market Sentiment Analysis Charts
          Container(
            height: 350, // Increased height to accommodate everything
            padding: EdgeInsets.all(16),
            child: Card(
              color: Colors.grey[850],
              child: Padding(
                padding: EdgeInsets.all(12),
                child: Column(
                  children: [
                    Text(
                      'Live Market Sentiment Analysis',
                      style: TextStyle(
                        fontSize: 16,
                        fontWeight: FontWeight.bold,
                        color: Colors.white,
                      ),
                    ),
                    SizedBox(height: 12),
                    Expanded(
                      child: Row(
                        children: [
                          Expanded(
                            flex: 1,
                            child: Column(
                              children: [
                                Text(
                                  'FinBERT',
                                  style: TextStyle(
                                    fontSize: 16,
                                    fontWeight: FontWeight.bold,
                                    color: Colors.blue,
                                  ),
                                ),
                                SizedBox(height: 8),
                                Expanded(
                                  child: _buildPieChart(
                                    controller.finbertPositiveCount.value,
                                    controller.finbertNegativeCount.value,
                                    controller.finbertNeutralCount.value,
                                    Colors.green,
                                    Colors.red,
                                    Colors.grey,
                                  ),
                                ),
                                SizedBox(height: 8),
                                _buildLegendRow(
                                  controller.finbertPositiveCount.value,
                                  controller.finbertNegativeCount.value,
                                  controller.finbertNeutralCount.value,
                                ),
                              ],
                            ),
                          ),
                          SizedBox(
                            width: 20,
                          ), // Increased spacing between charts
                          Expanded(
                            flex: 1,
                            child: Column(
                              children: [
                                Text(
                                  'VADER',
                                  style: TextStyle(
                                    fontSize: 16,
                                    fontWeight: FontWeight.bold,
                                    color: Colors.orange,
                                  ),
                                ),
                                SizedBox(height: 8),
                                Expanded(
                                  child: _buildPieChart(
                                    controller.vaderPositiveCount.value,
                                    controller.vaderNegativeCount.value,
                                    controller.vaderNeutralCount.value,
                                    Colors.green,
                                    Colors.red,
                                    Colors.grey,
                                  ),
                                ),
                                SizedBox(height: 8),
                                _buildLegendRow(
                                  controller.vaderPositiveCount.value,
                                  controller.vaderNegativeCount.value,
                                  controller.vaderNeutralCount.value,
                                ),
                              ],
                            ),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),

          // News List
          Expanded(
            child: Obx(() {
              if (controller.isLoading.isTrue) {
                return Center(child: CircularProgressIndicator());
              }
              if (controller.news.isEmpty) {
                return Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      Icon(Icons.radio, size: 64, color: Colors.grey[600]),
                      SizedBox(height: 16),
                      Text(
                        controller.news.isEmpty
                            ? 'No live news yet'
                            : 'No news in selected date range',
                        style: TextStyle(fontSize: 18, color: Colors.grey[600]),
                      ),
                      SizedBox(height: 8),
                      Text(
                        controller.news.isEmpty
                            ? 'Click refresh to fetch news'
                            : 'Try adjusting the date range',
                        style: TextStyle(fontSize: 14, color: Colors.grey[500]),
                      ),
                      SizedBox(height: 16),
                      ElevatedButton(
                        onPressed: () {
                          controller.fetchLiveNews();
                        },
                        child: controller.isSyncing.isFalse
                            ? Row(
                                mainAxisSize: MainAxisSize.min,
                                children: [
                                  Icon(Icons.sync),
                                  SizedBox(width: 8),
                                  Text('Fetch News'),
                                ],
                              )
                            : Row(
                                mainAxisSize: MainAxisSize.min,
                                children: [
                                  SizedBox(
                                    width: 16,
                                    height: 16,
                                    child: CircularProgressIndicator(
                                      strokeWidth: 2,
                                    ),
                                  ),
                                  SizedBox(width: 8),
                                  Text('Syncing...'),
                                ],
                              ),
                      ),
                    ],
                  ),
                );
              }
              return RefreshIndicator(
                onRefresh: () => controller.fetchLiveNews(),
                child: ListView.builder(
                  itemCount: controller.news.length,
                  itemBuilder: (context, index) {
                    final news = controller.news[index];
                    return Card(
                      margin: EdgeInsets.all(8),
                      child: Padding(
                        padding: EdgeInsets.all(16),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Row(
                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
                              children: [
                                Flexible(
                                  child: Text(
                                    news.source,
                                    style: TextStyle(
                                      fontSize: 12,
                                      fontWeight: FontWeight.bold,
                                      color: Colors.blue[300],
                                    ),
                                  ),
                                ),
                                Text(
                                  _formatDateTime(news.date),
                                  style: TextStyle(
                                    fontSize: 12,
                                    color: Colors.grey[600],
                                  ),
                                ),
                              ],
                            ),
                            SizedBox(height: 8),
                            Text(
                              news.title,
                              style: TextStyle(
                                fontSize: 16,
                                fontWeight: FontWeight.w600,
                              ),
                            ),
                            SizedBox(height: 12),
                            Row(
                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
                              children: [
                                Expanded(
                                  child: Column(
                                    crossAxisAlignment:
                                        CrossAxisAlignment.start,
                                    children: [
                                      Wrap(
                                        spacing: 8,
                                        children: [
                                          // FinBERT sentiment badge
                                          Container(
                                            padding: EdgeInsets.symmetric(
                                              horizontal: 8,
                                              vertical: 4,
                                            ),
                                            decoration: BoxDecoration(
                                              color: news.finbertSentimentColor
                                                  .withOpacity(0.2),
                                              border: Border.all(
                                                color:
                                                    news.finbertSentimentColor,
                                              ),
                                              borderRadius:
                                                  BorderRadius.circular(12),
                                            ),
                                            child: Row(
                                              mainAxisSize: MainAxisSize.min,
                                              children: [
                                                Text(
                                                  'F: ${news.finbertLabel.toUpperCase()} ',
                                                  style: TextStyle(
                                                    fontSize: 12,
                                                    color: news
                                                        .finbertSentimentColor,
                                                    fontWeight: FontWeight.w600,
                                                  ),
                                                ),
                                                Text(
                                                  '${(news.finbertScore * 100).round()}%',
                                                  style: TextStyle(
                                                    fontSize: 10,
                                                    color: news
                                                        .finbertSentimentColor,
                                                  ),
                                                ),
                                              ],
                                            ),
                                          ),
                                          // VADER sentiment badge
                                          Container(
                                            padding: EdgeInsets.symmetric(
                                              horizontal: 8,
                                              vertical: 4,
                                            ),
                                            decoration: BoxDecoration(
                                              color: news.vaderSentimentColor
                                                  .withOpacity(0.2),
                                              border: Border.all(
                                                color: news.vaderSentimentColor,
                                              ),
                                              borderRadius:
                                                  BorderRadius.circular(12),
                                            ),
                                            child: Row(
                                              mainAxisSize: MainAxisSize.min,
                                              children: [
                                                Text(
                                                  'V: ${news.vaderLabel.toUpperCase()} ',
                                                  style: TextStyle(
                                                    fontSize: 12,
                                                    color: news
                                                        .vaderSentimentColor,
                                                    fontWeight: FontWeight.w600,
                                                  ),
                                                ),
                                                Text(
                                                  '${(news.vaderScore * 100).round()}%',
                                                  style: TextStyle(
                                                    fontSize: 10,
                                                    color: news
                                                        .vaderSentimentColor,
                                                  ),
                                                ),
                                              ],
                                            ),
                                          ),
                                        ],
                                      ),
                                    ],
                                  ),
                                ),
                                ElevatedButton.icon(
                                  onPressed: () {
                                    controller.openUrl(news.url);
                                  },
                                  icon: Icon(Icons.open_in_new, size: 16),
                                  label: Text('Read'),
                                  style: ElevatedButton.styleFrom(
                                    backgroundColor: Colors.grey[800],
                                    foregroundColor: Colors.white,
                                    padding: EdgeInsets.symmetric(
                                      horizontal: 12,
                                      vertical: 8,
                                    ),
                                    shape: RoundedRectangleBorder(
                                      borderRadius: BorderRadius.circular(20),
                                    ),
                                  ),
                                ),
                              ],
                            ),
                          ],
                        ),
                      ),
                    );
                  },
                ),
              );
            }),
          ),
        ],
      ),
    );
  }

  // Widget to build a pie chart for sentiment
  Widget _buildPieChart(
    int positive,
    int negative,
    int neutral,
    Color positiveColor,
    Color negativeColor,
    Color neutralColor,
  ) {
    int total = positive + negative + neutral;
    if (total == 0) {
      return Center(
        child: Text(
          'No Data',
          style: TextStyle(fontSize: 12, color: Colors.grey[400]),
        ),
      );
    }

    List<PieChartSectionData> sections = [];

    if (positive > 0) {
      sections.add(
        PieChartSectionData(
          value: positive.toDouble(),
          color: positiveColor,
          title: '',
          radius: 40, // Reduced radius to prevent overlap
          borderSide: BorderSide(color: Colors.black, width: 1),
        ),
      );
    }

    if (negative > 0) {
      sections.add(
        PieChartSectionData(
          value: negative.toDouble(),
          color: negativeColor,
          title: '',
          radius: 40, // Reduced radius to prevent overlap
          borderSide: BorderSide(color: Colors.black, width: 1),
        ),
      );
    }

    if (neutral > 0) {
      sections.add(
        PieChartSectionData(
          value: neutral.toDouble(),
          color: neutralColor,
          title: '',
          radius: 40, // Reduced radius to prevent overlap
          borderSide: BorderSide(color: Colors.black, width: 1),
        ),
      );
    }

    return Container(
      padding: EdgeInsets.all(8),
      child: PieChart(
        PieChartData(
          sections: sections,
          centerSpaceRadius: 20, // Reduced center space
          sectionsSpace: 0, // No space between sections
          pieTouchData: PieTouchData(
            touchCallback: (FlTouchEvent event, pieTouchResponse) {},
          ),
          borderData: FlBorderData(show: false),
          startDegreeOffset: -90,
          centerSpaceColor: Colors.grey[850],
        ),
      ),
    );
  }

  // Widget to build the legend row
  Widget _buildLegendRow(int positive, int negative, int neutral) {
    int total = positive + negative + neutral;
    double positivePercent = total > 0 ? (positive / total) * 100 : 0;
    double negativePercent = total > 0 ? (negative / total) * 100 : 0;
    double neutralPercent = total > 0 ? (neutral / total) * 100 : 0;

    return Container(
      child: Column(
        children: [
          Container(
            height: 30,
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                _buildLegendItem('P', positive, Colors.green),
                _buildLegendItem('N', negative, Colors.red),
                _buildLegendItem('Ne', neutral, Colors.grey),
              ],
            ),
          ),
          SizedBox(height: 4),
          Container(
            height: 20,
            child: Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                Text(
                  '${positivePercent.toStringAsFixed(0)}%',
                  style: TextStyle(fontSize: 10, color: Colors.grey[400]),
                ),
                Text(
                  '${negativePercent.toStringAsFixed(0)}%',
                  style: TextStyle(fontSize: 10, color: Colors.grey[400]),
                ),
                Text(
                  '${neutralPercent.toStringAsFixed(0)}%',
                  style: TextStyle(fontSize: 10, color: Colors.grey[400]),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildLegendItem(String label, int count, Color color) {
    return Column(
      children: [
        Container(
          padding: EdgeInsets.only(bottom: 2),
          child: Text(
            '$count',
            style: TextStyle(fontSize: 10, color: Colors.white),
          ),
        ),
        Text(label, style: TextStyle(fontSize: 9, color: color)),
      ],
    );
  }

  String _formatDateTime(String dateTimeStr) {
    try {
      DateTime dateTime = DateTime.parse(dateTimeStr);
      return '${dateTime.year}/${dateTime.month.toString().padLeft(2, '0')}/${dateTime.day.toString().padLeft(2, '0')} ${dateTime.hour.toString().padLeft(2, '0')}:${dateTime.minute.toString().padLeft(2, '0')}';
    } catch (e) {
      return dateTimeStr;
    }
  }

  Future<void> _showDateRangePicker(BuildContext context) async {
    DateTime? pickedStartDate = await showDatePicker(
      context: context,
      initialDate: DateTime.now().subtract(
        Duration(days: 7),
      ), // Default to 7 days ago
      firstDate: DateTime(2020),
      lastDate: DateTime.now(),
    );

    if (pickedStartDate != null) {
      DateTime? pickedEndDate = await showDatePicker(
        context: context,
        initialDate: DateTime.now(), // Default to today
        firstDate: pickedStartDate,
        lastDate: DateTime.now(),
      );

      if (pickedEndDate != null) {
        String startDateStr =
            "${pickedStartDate.year}-${pickedStartDate.month.toString().padLeft(2, '0')}-${pickedStartDate.day.toString().padLeft(2, '0')}";
        String endDateStr =
            "${pickedEndDate.year}-${pickedEndDate.month.toString().padLeft(2, '0')}-${pickedEndDate.day.toString().padLeft(2, '0')}";

        controller.setDateRange(startDateStr, endDateStr);
      }
    }
  }
}
