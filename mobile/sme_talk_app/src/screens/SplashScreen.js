import React, { useEffect } from 'react';
import { View, Text, StyleSheet } from 'react-native';
import colors from '../theme/colors';

export default function SplashScreen({ onFinish }) {
  useEffect(() => {
    const timer = setTimeout(() => {
      onFinish();
    }, 2500);
    return () => clearTimeout(timer);
  }, []);

  return (
    <View style={styles.container}>
      <Text style={styles.logo}>🌿 SME-TALK</Text>
      <Text style={styles.subtitle}>ESG-Gold Platform · Algorand</Text>

      <View style={styles.badges}>
        <View style={[styles.badge, { backgroundColor: colors.environmental }]}>
          <Text style={styles.badgeText}>Environmental</Text>
        </View>
        <View style={[styles.badge, { backgroundColor: colors.social }]}>
          <Text style={styles.badgeText}>Social</Text>
        </View>
        <View style={[styles.badge, { backgroundColor: colors.governance }]}>
          <Text style={styles.badgeText}>Governance</Text>
        </View>
      </View>

      <Text style={styles.totalIssued}>총 발행 ESG-Gold</Text>
      <Text style={styles.totalValue}>1,250,000 ESGG</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.bg,
    alignItems: 'center',
    justifyContent: 'center',
    gap: 12,
  },
  logo: {
    fontSize: 36,
    fontWeight: 'bold',
    color: colors.gold,
  },
  subtitle: {
    fontSize: 14,
    color: colors.textMuted,
    marginBottom: 8,
  },
  badges: {
    flexDirection: 'row',
    gap: 8,
    marginVertical: 16,
  },
  badge: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 20,
  },
  badgeText: {
    color: colors.white,
    fontSize: 11,
    fontWeight: 'bold',
  },
  totalIssued: {
    color: colors.textMuted,
    fontSize: 13,
    marginTop: 16,
  },
  totalValue: {
    color: colors.goldLight,
    fontSize: 24,
    fontWeight: 'bold',
  },
});