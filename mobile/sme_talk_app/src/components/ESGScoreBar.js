import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import colors from '../theme/colors';

export default function ESGScoreBar({ e = 0, s = 0, g = 0 }) {
  const bars = [
    { label: 'E', value: e, color: colors.environmental },
    { label: 'S', value: s, color: colors.social },
    { label: 'G', value: g, color: colors.governance },
  ];

  return (
    <View style={styles.container}>
      {bars.map((bar) => (
        <View key={bar.label} style={styles.row}>
          <Text style={styles.label}>{bar.label}</Text>
          <View style={styles.track}>
            <View
              style={[
                styles.fill,
                { width: `${bar.value}%`, backgroundColor: bar.color },
              ]}
            />
          </View>
          <Text style={styles.value}>{bar.value}</Text>
        </View>
      ))}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    gap: 8,
  },
  row: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: 8,
  },
  label: {
    color: colors.textMuted,
    fontSize: 12,
    fontWeight: 'bold',
    width: 16,
  },
  track: {
    flex: 1,
    height: 8,
    backgroundColor: colors.surfaceLight,
    borderRadius: 4,
    overflow: 'hidden',
  },
  fill: {
    height: '100%',
    borderRadius: 4,
  },
  value: {
    color: colors.text,
    fontSize: 12,
    width: 28,
    textAlign: 'right',
  },
});