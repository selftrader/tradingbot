from services.institutional_flow import get_institutional_activity

def adjust_trade_signal_based_on_fii(symbol: str, ai_confidence: float):
    """Modify AI confidence based on FII/DII flow."""
    
    institutional_data = get_institutional_activity()
    net_fii = institutional_data["net_fii"]
    
    if net_fii > 5000:  # If FII buying is strong
        ai_confidence += 5
    elif net_fii < -5000:  # If FII selling is heavy
        ai_confidence -= 5

    return ai_confidence
