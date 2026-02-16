import 'package:flutter/material.dart';
import 'package:get/get.dart';
import '../../controllers/news_controller.dart';
import '../widgets/news_card.dart';
import '../widgets/sentiment_chart.dart';
import '../widgets/category_selector.dart';
import '../playground/playground_screen.dart';

class HomeScreen extends StatelessWidget {
  final NewsController newsController = Get.put(NewsController());

  HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[100],
      appBar: AppBar(
        title: ShaderMask(
          blendMode: BlendMode.srcIn,
          shaderCallback: (bounds) => LinearGradient(
            colors: [Colors.blue.shade400, Colors.purple.shade400],
          ).createShader(bounds),
          child: const Text(
            'CryptoPulse AI',
            style: TextStyle(
              fontWeight: FontWeight.bold,
              color: Colors.white,
              fontSize: 20,
            ),
          ),
        ),
        backgroundColor: const Color(0xFF1E293B),
        elevation: 0,
        iconTheme: const IconThemeData(color: Colors.white),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () => Get.to(() => PlaygroundScreen()),
        backgroundColor: Colors.blue.shade600,
        child: const Icon(Icons.science, color: Colors.white),
      ),
      body: Obx(() {
        if (newsController.isLoading.value) {
          return const Center(
            child: CircularProgressIndicator(
              valueColor: AlwaysStoppedAnimation<Color>(Colors.blue),
            ),
          );
        }

        if (newsController.newsList.isEmpty) {
          return Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(
                  Icons.article_outlined,
                  size: 64,
                  color: Colors.grey.shade600,
                ),
                const SizedBox(height: 16),
                Text(
                  'No news available',
                  style: TextStyle(fontSize: 18, color: Colors.grey.shade600),
                ),
              ],
            ),
          );
        }

        return Column(
          children: [
            // Sentiment Chart
            Container(
              margin: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: const Color(0xFF1E293B).withOpacity(0.5),
                borderRadius: BorderRadius.circular(16),
                border: Border.all(
                  color: Colors.grey.shade800.withOpacity(0.5),
                ),
                boxShadow: [
                  BoxShadow(
                    color: Colors.black.withOpacity(0.3),
                    blurRadius: 10,
                    offset: const Offset(0, 4),
                  ),
                ],
              ),
              child: SentimentChart(
                positive: newsController.positiveCount.value,
                negative: newsController.negativeCount.value,
                neutral: newsController.neutralCount.value,
              ),
            ),

            // Category Selector
            const CategorySelector(),

            // News List
            Expanded(
              child: ListView.builder(
                padding: const EdgeInsets.only(bottom: 16),
                itemCount:
                    newsController.newsList.length +
                    (newsController.hasMore.value ? 1 : 0),
                itemBuilder: (context, index) {
                  // Load More button at the end
                  if (index == newsController.newsList.length) {
                    return Obx(() {
                      if (newsController.isLoadingMore.value) {
                        return const Padding(
                          padding: EdgeInsets.all(16.0),
                          child: Center(
                            child: CircularProgressIndicator(
                              valueColor: AlwaysStoppedAnimation<Color>(
                                Colors.blue,
                              ),
                            ),
                          ),
                        );
                      }

                      return Padding(
                        padding: const EdgeInsets.all(16.0),
                        child: ElevatedButton(
                          onPressed: newsController.hasMore.value
                              ? () => newsController.loadMoreNews()
                              : null,
                          style: ElevatedButton.styleFrom(
                            backgroundColor: Colors.blue.shade600,
                            foregroundColor: Colors.white,
                            padding: const EdgeInsets.symmetric(
                              horizontal: 32,
                              vertical: 16,
                            ),
                            shape: RoundedRectangleBorder(
                              borderRadius: BorderRadius.circular(12),
                            ),
                          ),
                          child: const Text(
                            'load more',
                            style: TextStyle(
                              fontSize: 16,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ),
                      );
                    });
                  }

                  return NewsCard(news: newsController.newsList[index]);
                },
              ),
            ),
          ],
        );
      }),
    );
  }
}
