import 'dart:math';

class Stock {
  final String symbol;
  double price;

  Stock(this.symbol, this.price);

  void updatePrice(Random r) {
    final change = 0.95 + r.nextDouble() * 0.1; // -5% .. +5%
    price = double.parse((price * change).toStringAsFixed(2));
  }
}

class Portfolio {
  double cash;
  final Map<String, int> shares = {};

  Portfolio({this.cash = 1000.0});

  void buy(Stock s, int qty) {
    final cost = s.price * qty;
    if (cost > cash) throw Exception('Yetersiz bakiye');
    cash -= cost;
    shares[s.symbol] = (shares[s.symbol] ?? 0) + qty;
  }

  void sell(Stock s, int qty) {
    final have = shares[s.symbol] ?? 0;
    if (qty > have) throw Exception('Yetersiz hisse');
    shares[s.symbol] = have - qty;
    cash += s.price * qty;
  }

  double value(Map<String, Stock> market) {
    var v = cash;
    shares.forEach((sym, qty) {
      final s = market[sym];
      if (s != null) v += s.price * qty;
    });
    return double.parse(v.toStringAsFixed(2));
  }
}

class Market {
  final Map<String, Stock> stocks;
  final Random _r = Random();

  Market(this.stocks);

  void nextDay() {
    stocks.values.forEach((s) => s.updatePrice(_r));
  }
}
