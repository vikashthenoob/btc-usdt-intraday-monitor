"""Alert system for intraday trading signals."""

import logging
from typing import Dict, List, Optional
from enum import Enum
from datetime import datetime

logger = logging.getLogger(__name__)


class AlertSeverity(Enum):
    """Alert severity levels."""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


class AlertType(Enum):
    """Types of trading alerts."""
    PRICE_BREAKOUT = "price_breakout"
    RSI_OVERBOUGHT = "rsi_overbought"
    RSI_OVERSOLD = "rsi_oversold"
    MACD_CROSSOVER = "macd_crossover"
    BOLLINGER_BAND_TOUCH = "bollinger_band_touch"
    LIQUIDATION_SPIKE = "liquidation_spike"
    FUNDING_RATE_EXTREME = "funding_rate_extreme"
    VOLUME_SURGE = "volume_surge"


class Alert:
    """Represents a single trading alert."""
    
    def __init__(
        self,
        alert_type: AlertType,
        severity: AlertSeverity,
        symbol: str,
        message: str,
        price: float,
        timestamp: Optional[datetime] = None,
        metadata: Optional[Dict] = None
    ):
        self.alert_type = alert_type
        self.severity = severity
        self.symbol = symbol
        self.message = message
        self.price = price
        self.timestamp = timestamp or datetime.utcnow()
        self.metadata = metadata or {}
        self.acknowledged = False
    
    def to_dict(self) -> Dict:
        """Convert alert to dictionary."""
        return {
            'type': self.alert_type.value,
            'severity': self.severity.value,
            'symbol': self.symbol,
            'message': self.message,
            'price': self.price,
            'timestamp': self.timestamp.isoformat(),
            'metadata': self.metadata,
            'acknowledged': self.acknowledged
        }
    
    def __repr__(self) -> str:
        return f"Alert({self.alert_type.value}, {self.severity.value}, {self.symbol}, {self.message})"


class AlertManager:
    """Manages trading alerts and notifications."""
    
    def __init__(self, max_alerts: int = 1000):
        self.alerts: List[Alert] = []
        self.max_alerts = max_alerts
        self.subscribers: Dict[AlertType, List[callable]] = {}
    
    def subscribe(self, alert_type: AlertType, callback: callable) -> None:
        """Subscribe to alert notifications.
        
        Args:
            alert_type: Type of alert to subscribe to
            callback: Function to call when alert is triggered
        """
        if alert_type not in self.subscribers:
            self.subscribers[alert_type] = []
        self.subscribers[alert_type].append(callback)
        logger.debug(f"Subscribed to {alert_type.value}")
    
    def create_alert(
        self,
        alert_type: AlertType,
        severity: AlertSeverity,
        symbol: str,
        message: str,
        price: float,
        metadata: Optional[Dict] = None
    ) -> Alert:
        """Create and register a new alert.
        
        Args:
            alert_type: Type of alert
            severity: Severity level
            symbol: Trading symbol
            message: Alert message
            price: Current price
            metadata: Additional metadata
        
        Returns:
            Created Alert object
        """
        alert = Alert(alert_type, severity, symbol, message, price, metadata=metadata)
        self.alerts.append(alert)
        
        # Maintain max alerts limit
        if len(self.alerts) > self.max_alerts:
            self.alerts = self.alerts[-self.max_alerts:]
        
        logger.info(f"Alert created: {alert}")
        
        # Notify subscribers
        if alert_type in self.subscribers:
            for callback in self.subscribers[alert_type]:
                try:
                    callback(alert)
                except Exception as e:
                    logger.error(f"Error in alert callback: {e}")
        
        return alert
    
    def get_alerts(
        self,
        symbol: Optional[str] = None,
        severity: Optional[AlertSeverity] = None,
        alert_type: Optional[AlertType] = None,
        limit: int = 50
    ) -> List[Alert]:
        """Get alerts with optional filtering.
        
        Args:
            symbol: Filter by symbol
            severity: Filter by severity
            alert_type: Filter by alert type
            limit: Maximum number of alerts to return
        
        Returns:
            List of matching alerts (most recent first)
        """
        filtered = self.alerts
        
        if symbol:
            filtered = [a for a in filtered if a.symbol == symbol]
        
        if severity:
            filtered = [a for a in filtered if a.severity == severity]
        
        if alert_type:
            filtered = [a for a in filtered if a.alert_type == alert_type]
        
        return filtered[-limit:][::-1]  # Return most recent first
    
    def acknowledge_alert(self, alert: Alert) -> None:
        """Mark alert as acknowledged.
        
        Args:
            alert: Alert to acknowledge
        """
        alert.acknowledged = True
        logger.debug(f"Alert acknowledged: {alert}")
    
    def get_critical_alerts(self, symbol: Optional[str] = None) -> List[Alert]:
        """Get all unacknowledged critical alerts.
        
        Args:
            symbol: Optional symbol filter
        
        Returns:
            List of critical alerts
        """
        critical = [
            a for a in self.alerts
            if a.severity == AlertSeverity.CRITICAL and not a.acknowledged
        ]
        
        if symbol:
            critical = [a for a in critical if a.symbol == symbol]
        
        return critical
    
    def clear_old_alerts(self, keep_count: int = 500) -> int:
        """Remove old alerts to manage memory.
        
        Args:
            keep_count: Number of recent alerts to keep
        
        Returns:
            Number of alerts removed
        """
        removed = max(0, len(self.alerts) - keep_count)
        if removed > 0:
            self.alerts = self.alerts[-keep_count:]
            logger.info(f"Cleared {removed} old alerts")
        
        return removed


class AlertRuleEngine:
    """Evaluates trading conditions and triggers alerts."""
    
    def __init__(self, alert_manager: AlertManager):
        self.alert_manager = alert_manager
    
    def check_rsi_levels(
        self,
        symbol: str,
        rsi: float,
        price: float,
        overbought: float = 70,
        oversold: float = 30
    ) -> None:
        """Check RSI levels and create alerts.
        
        Args:
            symbol: Trading symbol
            rsi: Current RSI value
            price: Current price
            overbought: RSI overbought threshold
            oversold: RSI oversold threshold
        """
        if rsi >= overbought:
            self.alert_manager.create_alert(
                AlertType.RSI_OVERBOUGHT,
                AlertSeverity.WARNING,
                symbol,
                f"RSI {rsi:.2f} indicates overbought condition",
                price,
                {'rsi': rsi, 'threshold': overbought}
            )
        elif rsi <= oversold:
            self.alert_manager.create_alert(
                AlertType.RSI_OVERSOLD,
                AlertSeverity.WARNING,
                symbol,
                f"RSI {rsi:.2f} indicates oversold condition",
                price,
                {'rsi': rsi, 'threshold': oversold}
            )
    
    def check_bollinger_bands(
        self,
        symbol: str,
        price: float,
        upper_band: float,
        lower_band: float
    ) -> None:
        """Check Bollinger Band violations.
        
        Args:
            symbol: Trading symbol
            price: Current price
            upper_band: Upper band value
            lower_band: Lower band value
        """
        if price >= upper_band:
            self.alert_manager.create_alert(
                AlertType.BOLLINGER_BAND_TOUCH,
                AlertSeverity.INFO,
                symbol,
                f"Price {price} touched upper Bollinger Band",
                price,
                {'band': 'upper', 'band_value': upper_band}
            )
        elif price <= lower_band:
            self.alert_manager.create_alert(
                AlertType.BOLLINGER_BAND_TOUCH,
                AlertSeverity.INFO,
                symbol,
                f"Price {price} touched lower Bollinger Band",
                price,
                {'band': 'lower', 'band_value': lower_band}
            )
    
    def check_liquidation_spike(
        self,
        symbol: str,
        liquidation_volume: float,
        threshold: float,
        price: float
    ) -> None:
        """Check for liquidation spikes.
        
        Args:
            symbol: Trading symbol
            liquidation_volume: Current liquidation volume
            threshold: Volume threshold for spike detection
            price: Current price
        """
        if liquidation_volume > threshold:
            severity = AlertSeverity.CRITICAL if liquidation_volume > threshold * 2 else AlertSeverity.WARNING
            self.alert_manager.create_alert(
                AlertType.LIQUIDATION_SPIKE,
                severity,
                symbol,
                f"Liquidation spike detected: {liquidation_volume:.2f}",
                price,
                {'volume': liquidation_volume, 'threshold': threshold}
            )
