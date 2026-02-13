import 'package:flutter/material.dart';
import '../../models/news_model.dart';

class NewsCard extends StatelessWidget {
  final NewsModel news;

  const NewsCard({super.key, required this.news});

  @override
  Widget build(BuildContext context) {
    Color cardColor;
    IconData sentimentIcon;

    switch (news.sentimentLabel.toLowerCase()) {
      case 'positive':
        cardColor = Colors.green.shade100;
        sentimentIcon = Icons.sentiment_satisfied;
        break;
      case 'negative':
        cardColor = Colors.red.shade100;
        sentimentIcon = Icons.sentiment_dissatisfied;
        break;
      default:
        cardColor = Colors.grey.shade100;
        sentimentIcon = Icons.sentiment_neutral;
    }

    return Card(
      color: cardColor,
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(sentimentIcon, size: 20),
                const SizedBox(width: 8),
                Expanded(
                  child: Text(
                    news.title,
                    style: const TextStyle(
                      fontSize: 16,
                      fontWeight: FontWeight.bold,
                    ),
                    maxLines: 2,
                    overflow: TextOverflow.ellipsis,
                  ),
                ),
              ],
            ),
            const SizedBox(height: 8),
            Text(
              news.summary,
              style: const TextStyle(fontSize: 14),
              maxLines: 2,
              overflow: TextOverflow.ellipsis,
            ),
            const SizedBox(height: 8),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text(
                  news.source,
                  style: const TextStyle(fontSize: 12, color: Colors.grey),
                ),
                Text(
                  'Score: ${(news.sentimentScore * 100).toStringAsFixed(1)}%',
                  style: const TextStyle(
                    fontSize: 12,
                    fontWeight: FontWeight.w500,
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
