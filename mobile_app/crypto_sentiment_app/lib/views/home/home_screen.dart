import 'package:flutter/material.dart';
import 'package:get/get.dart';
import '../../controllers/news_controller.dart';
import '../widgets/news_card.dart';
import '../widgets/sentiment_chart.dart';

class HomeScreen extends StatelessWidget {
  final NewsController newsController = Get.put(NewsController());

  HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Crypto Sentiment'),
        backgroundColor: Colors.blue,
        foregroundColor: Colors.white,
      ),
      body: Obx(() {
        if (newsController.isLoading.value) {
          return const Center(child: CircularProgressIndicator());
        }

        if (newsController.newsList.isEmpty) {
          return const Center(child: Text('No news available'));
        }

        return Column(
          children: [
            SentimentChart(
              positive: newsController.positiveCount.value,
              negative: newsController.negativeCount.value,
              neutral: newsController.neutralCount.value,
            ),
            Expanded(
              child: ListView.builder(
                itemCount: newsController.newsList.length,
                itemBuilder: (context, index) {
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
