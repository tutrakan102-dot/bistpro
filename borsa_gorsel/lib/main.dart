import 'package:flutter/material.dart';
import 'dart:math';

void main() {
  runApp(const BorsaOyunu());
}

class BorsaOyunu extends StatelessWidget {
  const BorsaOyunu({super.key});

  @overrides
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: const BorsaEkrani(),
    );
  }
}

class BorsaEkrani extends StatefulWidget {
  const BorsaEkrani({super.key});

  @override
  State<BorsaEkrani> createState() => _BorsaEkraniState();
}

class _BorsaEkraniState extends State<BorsaEkrani> {
  double bakiye = 10000;
  double fiyat = 100;
  int lot = 0;
  final Random random = Random();

  void fiyatDegistir() {
    double degisim = random.nextDouble() * 10 - 5;
    fiyat += fiyat * degisim / 100;
  }

  void al() {
    if (bakiye >= fiyat) {
      setState(() {
        bakiye -= fiyat;
        lot++;
        fiyatDegistir();
      });
    }
  }

  void sat() {
    if (lot > 0) {
      setState(() {
        bakiye += fiyat;
        lot--;
        fiyatDegistir();
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("📈 Borsa Oyunu"),
        centerTitle: true,
      ),
      body: Center(
        child: Card(
          elevation: 6,
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(16),
          ),
          margin: const EdgeInsets.all(24),
          child: Padding(
            padding: const EdgeInsets.all(24),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                const Text(
                  "ABC HİSSESİ",
                  style: TextStyle(fontSize: 26, fontWeight: FontWeight.bold),
                ),
                const SizedBox(height: 16),

                Text(
                  "Fiyat\n${fiyat.toStringAsFixed(2)} TL",
                  textAlign: TextAlign.center,
                  style: const TextStyle(fontSize: 24),
                ),

                const SizedBox(height: 12),
                Text("Lot: $lot", style: const TextStyle(fontSize: 18)),
                Text(
                  "Bakiye: ${bakiye.toStringAsFixed(0)} TL",
                  style: const TextStyle(fontSize: 18),
                ),

                const SizedBox(height: 24),

                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                  children: [
                    ElevatedButton(
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.green,
                        padding: const EdgeInsets.symmetric(
                            horizontal: 24, vertical: 12),
                      ),
                      onPressed: al,
                      child: const Text("AL"),
                    ),
                    ElevatedButton(
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Colors.red,
                        padding: const EdgeInsets.symmetric(
                            horizontal: 24, vertical: 12),
                      ),
                      onPressed: sat,
                      child: const Text("SAT"),
                    ),
                  ],
                )
              ],
            ),
          ),
        ),
      ),
    );
  }
}