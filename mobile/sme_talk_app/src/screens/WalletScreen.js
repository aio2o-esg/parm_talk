import React, { useState } from 'react';
import {
  View, Text, ScrollView, TouchableOpacity,
  StyleSheet, Alert
} from 'react-native';
import colors from '../theme/colors';
import BottomNav from '../components/BottomNav';

const ASSETS = [
  { name: 'ESG-Gold', symbol: 'ESGG', amount: 3250, krw: 162500, asaId: '12345678' },
  { name: 'Green Point', symbol: 'GP', amount: 820, krw: 8200, asaId: '87654321' },
  { name: 'ALGO', symbol: 'ALGO', amount: 5.2, krw: 5720, asaId: 'native' },
];

const TRANSACTIONS = [
  { type: 'receive', desc: 'ESG 활동 보상', amount: '+50 ESGG', time: '2026.03.31 14:32', txHash: 'ABC123...XYZ' },
  { type: 'receive', desc: 'ESG 활동 보상', amount: '+32 ESGG', time: '2026.03.31 09:15', txHash: 'DEF456...UVW' },
  { type: 'send', desc: '지역화폐 전환', amount: '-100 ESGG', time: '2026.03.30 18:00', txHash: 'GHI789...RST' },
  { type: 'receive', desc: 'ESG 활동 보상', amount: '+30 ESGG', time: '2026.03.30 17:44', txHash: 'JKL012...OPQ' },
];

export default function WalletScreen({ onNavigate }) {
  const address = 'ALGO7X...K9MN';

  return (
    <View style={styles.container}>
      <ScrollView style={styles.scroll} showsVerticalScrollIndicator={false}>
        <Text style={styles.title}>지갑 / 온체인 자산</Text>

        {/* 계정 주소 */}
        <TouchableOpacity
          style={styles.addressBox}
          onPress={() => Alert.alert('주소 복사', 'Algorand 주소가 복사되었습니다.')}
        >
          <Text style={styles.addressLabel}>Algorand 계정 주소</Text>
          <Text style={styles.address}>{address} 📋</Text>
        </TouchableOpacity>

        {/* 총 자산 */}
        <View style={styles.totalBox}>
          <Text style={styles.totalLabel}>총 ESG-Gold</Text>
          <Text style={styles.totalAmount}>3,250 ESGG</Text>
          <Text style={styles.totalKrw}>≈ 162,500 원</Text>
        </View>

        {/* 빠른 실행 */}
        <View style={styles.quickBtns}>
          {['↑ 보내기', '↓ 받기', '⇄ 교환', '📋 내역'].map((btn, i) => (
            <TouchableOpacity key={i} style={styles.quickBtn}>
              <Text style={styles.quickBtnText}>{btn}</Text>
            </TouchableOpacity>
          ))}
        </View>

        {/* 보유 자산 목록 */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>보유 자산 (ASA)</Text>
          {ASSETS.map((asset, i) => (
            <View key={i} style={styles.assetItem}>
              <View>
                <Text style={styles.assetName}>{asset.name}</Text>
                <Text style={styles.assetId}>ASA: {asset.asaId}</Text>
              </View>
              <View style={styles.assetRight}>
                <Text style={styles.assetAmount}>{asset.amount.toLocaleString()} {asset.symbol}</Text>
                <Text style={styles.assetKrw}>≈ {asset.krw.toLocaleString()} 원</Text>
              </View>
            </View>
          ))}
        </View>

        {/* 온체인 거래 내역 */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>온체인 거래 내역</Text>
          {TRANSACTIONS.map((tx, i) => (
            <View key={i} style={styles.txItem}>
              <View>
                <Text style={styles.txDesc}>{tx.desc}</Text>
                <Text style={styles.txHash}>TX: {tx.txHash}</Text>
                <Text style={styles.txTime}>{tx.time}</Text>
              </View>
              <Text style={[
                styles.txAmount,
                tx.type === 'receive' ? styles.txReceive : styles.txSend
              ]}>
                {tx.amount}
              </Text>
            </View>
          ))}

          <TouchableOpacity style={styles.explorerBtn}>
            <Text style={styles.explorerBtnText}>블록탐색기 →</Text>
          </TouchableOpacity>
        </View>
      </ScrollView>

      <BottomNav active="wallet" onPress={onNavigate} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.bg },
  scroll: { flex: 1, padding: 20 },
  title: { color: colors.gold, fontSize: 22, fontWeight: 'bold', marginBottom: 16 },
  addressBox: {
    backgroundColor: colors.surface, borderRadius: 12,
    padding: 14, marginBottom: 12,
    borderWidth: 1, borderColor: colors.border,
  },
  addressLabel: { color: colors.textMuted, fontSize: 11, marginBottom: 4 },
  address: { color: colors.gold, fontSize: 14, fontWeight: 'bold' },
  totalBox: {
    backgroundColor: colors.surfaceLight, borderRadius: 16,
    padding: 20, alignItems: 'center', marginBottom: 16,
    borderWidth: 1, borderColor: colors.gold,
  },
  totalLabel: { color: colors.textMuted, fontSize: 13 },
  totalAmount: { color: colors.goldLight, fontSize: 32, fontWeight: 'bold' },
  totalKrw: { color: colors.textMuted, fontSize: 13 },
  quickBtns: {
    flexDirection: 'row', gap: 8, marginBottom: 16,
  },
  quickBtn: {
    flex: 1, backgroundColor: colors.surface, borderRadius: 12,
    padding: 12, alignItems: 'center',
    borderWidth: 1, borderColor: colors.border,
  },
  quickBtnText: { color: colors.gold, fontSize: 12, fontWeight: 'bold' },
  section: {
    backgroundColor: colors.surface, borderRadius: 16,
    padding: 16, marginBottom: 16,
    borderWidth: 1, borderColor: colors.border,
  },
  sectionTitle: { color: colors.gold, fontSize: 14, fontWeight: 'bold', marginBottom: 12 },
  assetItem: {
    flexDirection: 'row', justifyContent: 'space-between',
    alignItems: 'center', paddingVertical: 10,
    borderBottomWidth: 1, borderBottomColor: colors.border,
  },
  assetName: { color: colors.text, fontSize: 14, fontWeight: 'bold' },
  assetId: { color: colors.textMuted, fontSize: 11 },
  assetRight: { alignItems: 'flex-end' },
  assetAmount: { color: colors.goldLight, fontSize: 14, fontWeight: 'bold' },
  assetKrw: { color: colors.textMuted, fontSize: 11 },
  txItem: {
    flexDirection: 'row', justifyContent: 'space-between',
    alignItems: 'center', paddingVertical: 10,
    borderBottomWidth: 1, borderBottomColor: colors.border,
  },
  txDesc: { color: colors.text, fontSize: 13, fontWeight: 'bold' },
  txHash: { color: colors.info, fontSize: 11 },
  txTime: { color: colors.textMuted, fontSize: 11 },
  txAmount: { fontSize: 14, fontWeight: 'bold' },
  txReceive: { color: colors.success },
  txSend: { color: colors.danger },
  explorerBtn: {
    marginTop: 12, alignItems: 'center',
    padding: 10,
  },
  explorerBtnText: { color: colors.info, fontSize: 13 },
});