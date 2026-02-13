class NewsModel {
  final int id;
  final String title;
  final String summary;
  final String source;
  final String url;
  final String publishedDate;
  final String sentimentLabel;
  final double sentimentScore;

  NewsModel({
    required this.id,
    required this.title,
    required this.summary,
    required this.source,
    required this.url,
    required this.publishedDate,
    required this.sentimentLabel,
    required this.sentimentScore,
  });

  /// Creates a NewsModel instance from JSON data
  factory NewsModel.fromJson(Map<String, dynamic> json) {
    return NewsModel(
      id: json['id'] as int? ?? 0,
      title: json['title'] as String? ?? '',
      summary: json['summary'] as String? ?? '',
      source: json['source'] as String? ?? '',
      url: json['url'] as String? ?? '',
      publishedDate: json['published_date'] as String? ?? '',
      sentimentLabel: json['sentiment_label'] as String? ?? 'neutral',
      sentimentScore: (json['sentiment_score'] as num?)?.toDouble() ?? 0.0,
    );
  }

  /// Converts NewsModel instance to JSON
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'title': title,
      'summary': summary,
      'source': source,
      'url': url,
      'published_date': publishedDate,
      'sentiment_label': sentimentLabel,
      'sentiment_score': sentimentScore,
    };
  }

  /// Get sentiment color based on label
  String get sentimentColor {
    switch (sentimentLabel.toLowerCase()) {
      case 'positive':
        return 'green';
      case 'negative':
        return 'red';
      default:
        return 'grey';
    }
  }

  /// Get sentiment emoji based on label
  String get sentimentEmoji {
    switch (sentimentLabel.toLowerCase()) {
      case 'positive':
        return '😊';
      case 'negative':
        return '😞';
      default:
        return '😐';
    }
  }
}
