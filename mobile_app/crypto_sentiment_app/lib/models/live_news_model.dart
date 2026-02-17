import 'package:flutter/material.dart';

class LiveNewsModel {
  final int id;
  final String title;
  final String text;
  final String summary;
  final String url;
  final String source;
  final String date;
  final String sentiment;
  final String sentimentLabel;
  final double sentimentScore;
  final String vaderLabel;
  final double vaderScore;
  final String finbertLabel;
  final double finbertScore;

  LiveNewsModel({
    required this.id,
    required this.title,
    required this.text,
    required this.summary,
    required this.url,
    required this.source,
    required this.date,
    required this.sentiment,
    required this.sentimentLabel,
    required this.sentimentScore,
    required this.vaderLabel,
    required this.vaderScore,
    required this.finbertLabel,
    required this.finbertScore,
  });

  /// Creates a LiveNewsModel instance from JSON data
  factory LiveNewsModel.fromJson(Map<String, dynamic> json) {
    return LiveNewsModel(
      id: json['id'] as int? ?? 0,
      title: json['title'] as String? ?? '',
      text: json['text'] as String? ?? '',
      summary: json['summary'] as String? ?? '',
      url: json['url'] as String? ?? '',
      source: json['source'] as String? ?? '',
      date: json['date'] as String? ?? '',
      sentiment: json['sentiment'] as String? ?? '{}',
      sentimentLabel: json['sentiment_label'] as String? ?? 'neutral',
      sentimentScore: (json['sentiment_score'] as num?)?.toDouble() ?? 0.0,
      vaderLabel: json['vader_label'] as String? ?? 'neutral',
      vaderScore: (json['vader_score'] as num?)?.toDouble() ?? 0.0,
      finbertLabel: json['finbert_label'] as String? ?? 'neutral',
      finbertScore: (json['finbert_score'] as num?)?.toDouble() ?? 0.0,
    );
  }

  /// Converts LiveNewsModel instance to JSON
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'title': title,
      'text': text,
      'summary': summary,
      'url': url,
      'source': source,
      'date': date,
      'sentiment': sentiment,
      'sentiment_label': sentimentLabel,
      'sentiment_score': sentimentScore,
      'vader_label': vaderLabel,
      'vader_score': vaderScore,
      'finbert_label': finbertLabel,
      'finbert_score': finbertScore,
    };
  }

  /// Get FinBERT sentiment color based on label
  Color get finbertSentimentColor {
    switch (finbertLabel.toLowerCase()) {
      case 'positive':
        return Colors.green;
      case 'negative':
        return Colors.red;
      default:
        return Colors.grey;
    }
  }

  /// Get VADER sentiment color based on label
  Color get vaderSentimentColor {
    switch (vaderLabel.toLowerCase()) {
      case 'positive':
        return Colors.green;
      case 'negative':
        return Colors.red;
      default:
        return Colors.grey;
    }
  }

  /// Get FinBERT sentiment emoji based on label
  String get finbertSentimentEmoji {
    switch (finbertLabel.toLowerCase()) {
      case 'positive':
        return '😊';
      case 'negative':
        return '😞';
      default:
        return '😐';
    }
  }

  /// Get VADER sentiment emoji based on label
  String get vaderSentimentEmoji {
    switch (vaderLabel.toLowerCase()) {
      case 'positive':
        return '😊';
      case 'negative':
        return '😞';
      default:
        return '😐';
    }
  }
}
