import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet } from 'react-native';
import colors from '../theme/colors';

export default function GoldCard({ balance = 0, asaId = '-', onSend, onReceive, onExchange }) {
  return (
    <View style={styles.card}>
      <View style={styles.header}>
        <Text style={styles.title}>ESG-Gold 잔액</Text>
        <Text style={styles.asaId}>ASA ID: {asaId}</Text>
      </View>

      <Text style={styles.balance}>{balance.toLocaleString()}</Text>
      <Text style={styles.unit}>ESGG</Text>

      <View style={styles.buttons}>
        <TouchableOpacity style={styles.btn} onPress={onSend}>
          <Text style={styles.btnIcon}>↑</Text>
          <Text style={styles.btnLabel}>보내기</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.btn} onPress={onReceive}>
          <Text style={styles.btnIcon}>↓</Text>
          <Text style={styles.btnLabel}>받기</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.btn} onPress={onExchange}>
          <Text style={styles.btnIcon}>⇄</Text>
          <Text style={styles.btnLabel}>교환</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: colors.surfaceLight,
    borderRadius: 16,
    padding: 20,
    borderWidth: 1,
    borderColor: colors.gold,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 12,
  },
  title: {
    color: colors.gold,
    fontSize: 14,
    fontWeight: 'bold',
  },
  asaId: {
    color: colors.textMuted,
    fontSize: 11,
  },
  balance: {
    color: colors.goldLight,
    fontSize: 36,
    fontWeight: 'bold',
    textAlign: 'center',
  },
  unit: {
    color: colors.textMuted,
    fontSize: 14,
    textAlign: 'center',
    marginBottom: 16,
  },
  buttons: {
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
  btn: {
    alignItems: 'center',
    backgroundColor: colors.surface,
    borderRadius: 12,
    paddingVertical: 8,
    paddingHorizontal: 20,
  },
  btnIcon: {
    color: colors.gold,
    fontSize: 18,
    fontWeight: 'bold',
  },
  btnLabel: {
    color: colors.text,
    fontSize: 11,
    marginTop: 2,
  },
});