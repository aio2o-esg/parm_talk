import React from 'react';
import { View, TouchableOpacity, Text, StyleSheet } from 'react-native';
import colors from '../theme/colors';

const tabs = [
  { name: 'home', label: '홈', icon: '🏠' },
  { name: 'activity', label: '활동', icon: '🌿' },
  { name: 'wallet', label: '지갑', icon: '💰' },
  { name: 'policy', label: '정책', icon: '📊' },
  { name: 'mypage', label: '마이', icon: '👤' },
];

export default function BottomNav({ active, onPress }) {
  return (
    <View style={styles.container}>
      {tabs.map((tab) => (
        <TouchableOpacity
          key={tab.name}
          style={styles.tab}
          onPress={() => onPress(tab.name)}
        >
          <Text style={styles.icon}>{tab.icon}</Text>
          <Text style={[
            styles.label,
            active === tab.name && styles.labelActive
          ]}>
            {tab.label}
          </Text>
        </TouchableOpacity>
      ))}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    backgroundColor: colors.surface,
    borderTopWidth: 1,
    borderTopColor: colors.border,
    paddingBottom: 20,
    paddingTop: 10,
  },
  tab: {
    flex: 1,
    alignItems: 'center',
  },
  icon: {
    fontSize: 20,
    marginBottom: 2,
  },
  label: {
    fontSize: 11,
    color: colors.textMuted,
  },
  labelActive: {
    color: colors.gold,
    fontWeight: 'bold',
  },
});