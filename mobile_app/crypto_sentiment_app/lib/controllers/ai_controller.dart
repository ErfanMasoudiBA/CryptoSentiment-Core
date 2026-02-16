import 'package:get/get.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

class AIController extends GetxController {
  var resultLabel = ''.obs;
  var resultScore = 0.0.obs;
  var isLoading = false.obs;

  static const String _baseUrl = 'http://10.0.2.2:8000';

  Future<void> analyzeText(String text, String model) async {
    if (text.trim().isEmpty) {
      Get.snackbar(
        'Error',
        'Please enter some text to analyze.',
        snackPosition: SnackPosition.BOTTOM,
      );
      return;
    }

    isLoading(true);
    resultLabel('');
    resultScore(0.0);

    try {
      final response = await http.post(
        Uri.parse('$_baseUrl/api/analyze_text'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          'text': text.trim(),
          'model': model,
        }),
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body) as Map<String, dynamic>;
        resultLabel.value = (data['label'] as String? ?? 'neutral');
        resultScore.value = (data['score'] as num?)?.toDouble() ?? 0.0;
      } else {
        Get.snackbar(
          'Error',
          'Failed to analyze: ${response.statusCode}',
          snackPosition: SnackPosition.BOTTOM,
        );
      }
    } catch (e) {
      Get.snackbar(
        'Network Error',
        'Could not reach server. Is the backend running on 10.0.2.2:8000?',
        snackPosition: SnackPosition.BOTTOM,
      );
    } finally {
      isLoading(false);
    }
  }

  void clearResult() {
    resultLabel('');
    resultScore(0.0);
  }
}
