import 'dart:io';
import 'package:borsa_oyunu/borsa_oyunu.dart';

void main(List<String> arguments) {
  final market = Market({
    'ALFA': Stock('ALFA', 100.0),
    'BETA': Stock('BETA', 50.0),
    'GAMMA': Stock('GAMMA', 25.0),
  });

  final portfolio = Portfolio();

  print('Borsa Oyunu - Basit Konsol Sürümü');
  print('Komutlar: l=list market, p=portfolio, b SYMBOL QTY, s SYMBOL QTY, n=next day, q=quit, h=help');

  while (true) {
    stdout.write('> ');
    final line = stdin.readLineSync();
    if (line == null) break;
    final parts = line.trim().split(RegExp(r'\s+'));
    if (parts.isEmpty || parts[0] == '') continue;
    final cmd = parts[0].toLowerCase();

    try {
      if (cmd == 'q') break;
      else if (cmd == 'h') {
        print('h: yardım, l: piyasayı listele, p: portföy, b SYMBOL QTY: al, s SYMBOL QTY: sat, n: gün ilerlet');
      } else if (cmd == 'l') {
        market.stocks.forEach((k, v) => print('${v.symbol}: ${v.price} TL'));
      } else if (cmd == 'p') {
        print('Nakit: ${portfolio.cash} TL');
        if (portfolio.shares.isEmpty) print('Hiç hisse yok');
        portfolio.shares.forEach((k, v) => print('$k: $v'));
        print('Toplam değer: ${portfolio.value(market.stocks)} TL');
      } else if (cmd == 'b' && parts.length >= 3) {
        final sym = parts[1].toUpperCase();
        final qty = int.tryParse(parts[2]) ?? 0;
        final s = market.stocks[sym];
        if (s == null) print('Hisse bulunamadı: $sym');
        else {
          portfolio.buy(s, qty);
          print('Alındı: $qty x ${s.symbol} @ ${s.price}');
        }
      } else if (cmd == 's' && parts.length >= 3) {
        final sym = parts[1].toUpperCase();
        final qty = int.tryParse(parts[2]) ?? 0;
        final s = market.stocks[sym];
        if (s == null) print('Hisse bulunamadı: $sym');
        else {
          portfolio.sell(s, qty);
          print('Satıldı: $qty x ${s.symbol} @ ${s.price}');
        }
      } else if (cmd == 'n') {
        market.nextDay();
        print('Gün ilerledi. Yeni fiyatlar:');
        market.stocks.forEach((k, v) => print('${v.symbol}: ${v.price} TL'));
      } else {
        print('Bilinmeyen komut, yardım için h');
      }
    } catch (e) {
      print('Hata: $e');
    }
  }

  print('Oyun kapandı. Son değer: ${portfolio.value(market.stocks)} TL');
}
