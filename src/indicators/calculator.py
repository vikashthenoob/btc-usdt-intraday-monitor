"""Technical indicators calculator for intraday analysis."""

import logging
from typing import List, Tuple, Optional
import statistics

logger = logging.getLogger(__name__)


class IndicatorCalculator:
    """Calculates technical indicators from price data."""
    
    @staticmethod
    def sma(prices: List[float], period: int = 20) -> List[Optional[float]]:
        """Simple Moving Average.
        
        Args:
            prices: List of closing prices
            period: Number of periods for averaging
        
        Returns:
            List of SMA values (None for insufficient data)
        """
        sma_values = [None] * (period - 1)
        
        for i in range(period - 1, len(prices)):
            window = prices[i - period + 1:i + 1]
            sma_values.append(statistics.mean(window))
        
        return sma_values
    
    @staticmethod
    def ema(prices: List[float], period: int = 20) -> List[Optional[float]]:
        """Exponential Moving Average.
        
        Args:
            prices: List of closing prices
            period: Number of periods for averaging
        
        Returns:
            List of EMA values (None for insufficient data)
        """
        if len(prices) < period:
            return [None] * len(prices)
        
        multiplier = 2 / (period + 1)
        ema_values = [None] * (period - 1)
        
        # Start with SMA for first EMA value
        ema_values.append(statistics.mean(prices[:period]))
        
        for i in range(period, len(prices)):
            ema = prices[i] * multiplier + ema_values[-1] * (1 - multiplier)
            ema_values.append(ema)
        
        return ema_values
    
    @staticmethod
    def rsi(prices: List[float], period: int = 14) -> List[Optional[float]]:
        """Relative Strength Index.
        
        Args:
            prices: List of closing prices
            period: Number of periods (typically 14)
        
        Returns:
            List of RSI values (0-100)
        """
        if len(prices) < period + 1:
            return [None] * len(prices)
        
        rsi_values = [None] * period
        gains = []
        losses = []
        
        # Calculate price changes
        for i in range(1, len(prices)):
            change = prices[i] - prices[i - 1]
            gains.append(change if change > 0 else 0)
            losses.append(-change if change < 0 else 0)
        
        # Calculate initial average gain and loss
        avg_gain = statistics.mean(gains[:period])
        avg_loss = statistics.mean(losses[:period])
        
        for i in range(period, len(prices)):
            if avg_loss == 0:
                rsi = 100 if avg_gain > 0 else 50
            else:
                rs = avg_gain / avg_loss
                rsi = 100 - (100 / (1 + rs))
            
            rsi_values.append(rsi)
            
            # Update averages using smoothing
            avg_gain = (avg_gain * (period - 1) + gains[i]) / period
            avg_loss = (avg_loss * (period - 1) + losses[i]) / period
        
        return rsi_values
    
    @staticmethod
    def macd(prices: List[float], fast: int = 12, slow: int = 26, signal: int = 9) -> Tuple[List, List, List]:
        """MACD (Moving Average Convergence Divergence).
        
        Args:
            prices: List of closing prices
            fast: Fast EMA period (typically 12)
            slow: Slow EMA period (typically 26)
            signal: Signal line EMA period (typically 9)
        
        Returns:
            Tuple of (MACD line, Signal line, Histogram)
        """
        fast_ema = IndicatorCalculator.ema(prices, fast)
        slow_ema = IndicatorCalculator.ema(prices, slow)
        
        # MACD line is difference between fast and slow EMA
        macd_line = [f - s if f is not None and s is not None else None 
                     for f, s in zip(fast_ema, slow_ema)]
        
        # Signal line is EMA of MACD line
        macd_cleaned = [x for x in macd_line if x is not None]
        signal_line = IndicatorCalculator.ema(macd_cleaned, signal)
        
        # Histogram is difference between MACD and Signal
        histogram = [m - sig if m is not None and sig is not None else None
                    for m, sig in zip(macd_line[-len(signal_line):], signal_line)]
        
        return macd_line, signal_line, histogram
    
    @staticmethod
    def bollinger_bands(prices: List[float], period: int = 20, std_dev: float = 2.0) -> Tuple[List, List, List]:
        """Bollinger Bands.
        
        Args:
            prices: List of closing prices
            period: Period for SMA and standard deviation
            std_dev: Number of standard deviations (typically 2)
        
        Returns:
            Tuple of (Upper band, Middle band, Lower band)
        """
        sma_values = IndicatorCalculator.sma(prices, period)
        
        upper_band = []
        lower_band = []
        middle_band = []
        
        for i in range(len(prices)):
            if sma_values[i] is None:
                upper_band.append(None)
                lower_band.append(None)
                middle_band.append(None)
            else:
                # Calculate standard deviation for the window
                window = prices[i - period + 1:i + 1]
                std = statistics.stdev(window) if len(window) > 1 else 0
                
                middle = sma_values[i]
                upper = middle + (std_dev * std)
                lower = middle - (std_dev * std)
                
                upper_band.append(upper)
                lower_band.append(lower)
                middle_band.append(middle)
        
        return upper_band, middle_band, lower_band
    
    @staticmethod
    def atr(highs: List[float], lows: List[float], closes: List[float], period: int = 14) -> List[Optional[float]]:
        """Average True Range.
        
        Args:
            highs: List of high prices
            lows: List of low prices
            closes: List of closing prices
            period: Period for averaging (typically 14)
        
        Returns:
            List of ATR values
        """
        if len(highs) < period:
            return [None] * len(highs)
        
        true_ranges = []
        atr_values = [None] * period
        
        for i in range(1, len(closes)):
            tr = max(
                highs[i] - lows[i],
                abs(highs[i] - closes[i - 1]),
                abs(lows[i] - closes[i - 1])
            )
            true_ranges.append(tr)
        
        # Initial ATR
        atr = statistics.mean(true_ranges[:period])
        atr_values.append(atr)
        
        # Subsequent ATR values
        for i in range(period, len(true_ranges)):
            atr = (atr * (period - 1) + true_ranges[i]) / period
            atr_values.append(atr)
        
        return atr_values
