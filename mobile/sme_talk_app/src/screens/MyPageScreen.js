import React from 'react';
import {
  View, Text, ScrollView, TouchableOpacity,
  StyleSheet, Alert
} from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import colors from '../theme/colors';
import ESGScoreBar from '../components/ESGScoreBar';
import BottomNav from '../components/BottomNav';

const MENU_ITEMS = [
  { icon: '🔔', label: '알림 설정' },
  { icon: '🔒', label: '보안 및 개인정보' },
  { icon: '❓', label: '고객센터 / FAQ' },
];

export default function MyPageScreen({ user, onNavigate, onLogout }) {
  const handleLogout = async () => {
    Alert.alert('로그아웃', '로그아웃 하시겠습니까?', [
      { text: '취소', style: 'cancel' },
      {
        text: '로그아웃',
        style: 'destructive',
        onPress: async () => {
          await AsyncStorage.removeItem('access_token');
          onLogout();
        },
      },
    ]);
  };

  const isMerchant = user?.userType === 'merchant';

  return (
    <View style={styles.container}>
      <ScrollView style={styles.scroll} showsVerticalScrollIndicator={false}>
        <Text style={styles.title}>마이페이지</Text>

        {/* 프로필 카드 */}
        <View style={styles.profileCard}>
          <Text style={styles.profileIcon}>👤</Text>
          <View>
            <Text style={styles.profileName}>{user?.name || '사용자'}</Text>
            <Text style={styles.profileType}>
              {user?.userType === 'admin' ? '지자체 관리자'
                : user?.userType === 'merchant' ? '소상공인'
                : '시민'} · {user?.region || '서울시'}
            </Text>
          </View>
        </View>

        {/* 요약 통계 */}
        <View style={styles.statsRow}>
          <View style={styles.statItem}>
            <Text style={styles.statValue}>3,250</Text>
            <Text style={styles.statLabel}>ESG-Gold</Text>
          </View>
          <View style={styles.statDivider} />
          <View style={styles.statItem}>
            <Text style={styles.statValue}>28</Text>
            <Text style={styles.statLabel}>인증 횟수</Text>
          </View>
          <View style={styles.statDivider} />
          <View style={styles.statItem}>
            <Text style={styles.statValue}>72점</Text>
            <Text style={styles.statLabel}>ESG 등급</Text>
          </View>
        </View>

        {/* ESG 점수 세부 */}
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <Text style={styles.sectionTitle}>ESG 점수 세부 현황</Text>
            <TouchableOpacity>
              <Text style={styles.historyBtn}>점수 이력 보기 →</Text>
            </TouchableOpacity>
          </View>
          <ESGScoreBar e={72} s={65} g={58} />
        </View>

        {/* Algorand 지갑 */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Algorand 지갑 연결</Text>
          <View style={styles.walletRow}>
            <View>
              <Text style={styles.walletAddress}>ALGO7X...K9MN</Text>
              <Text style={styles.walletStatus}>✅ 연결됨</Text>
            </View>
            <TouchableOpacity style={styles.walletBtn}>
              <Text style={styles.walletBtnText}>관리</Text>
            </TouchableOpacity>
          </View>
        </View>

        {/* 소상공인 전용: 사업장 정보 */}
        {isMerchant && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>사업장 정보</Text>
            <TouchableOpacity style={styles.merchantBtn}>
              <Text style={styles.merchantBtnText}>✏️ 사업장 정보 수정</Text>
            </TouchableOpacity>
          </View>
        )}

        {/* 메뉴 항목 */}
        <View style={styles.section}>
          {MENU_ITEMS.map((item, i) => (
            <TouchableOpacity
              key={i}
              style={[
                styles.menuItem,
                i < MENU_ITEMS.length - 1 && styles.menuItemBorder
              ]}
            >
              <Text style={styles.menuIcon}>{item.icon}</Text>
              <Text style={styles.menuLabel}>{item.label}</Text>
              <Text style={styles.menuArrow}>›</Text>
            </TouchableOpacity>
          ))}
        </View>

        {/* 로그아웃 */}
        <TouchableOpacity style={styles.logoutBtn} onPress={handleLogout}>
          <Text style={styles.logoutText}>로그아웃</Text>
        </TouchableOpacity>

      </ScrollView>

      <BottomNav active="mypage" onPress={onNavigate} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.bg },
  scroll: { flex: 1, padding: 20 },
  title: { color: colors.gold, fontSize: 22, fontWeight: 'bold', marginBottom: 16 },
  profileCard: {
    flexDirection: 'row', alignItems: 'center', gap: 14,
    backgroundColor: colors.surface, borderRadius: 16,
    padding: 16, marginBottom: 12,
    borderWidth: 1, borderColor: colors.border,
  },
  profileIcon: { fontSize: 40 },
  profileName: { color: colors.text, fontSize: 18, fontWeight: 'bold' },
  profileType: { color: colors.textMuted, fontSize: 13, marginTop: 2 },
  statsRow: {
    flexDirection: 'row', backgroundColor: colors.surface,
    borderRadius: 16, padding: 16, marginBottom: 12,
    borderWidth: 1, borderColor: colors.border,
  },
  statItem: { flex: 1, alignItems: 'center' },
  statValue: { color: colors.goldLight, fontSize: 18, fontWeight: 'bold' },
  statLabel: { color: colors.textMuted, fontSize: 11, marginTop: 2 },
  statDivider: { width: 1, backgroundColor: colors.border },
  section: {
    backgroundColor: colors.surface, borderRadius: 16,
    padding: 16, marginBottom: 12,
    borderWidth: 1, borderColor: colors.border,
  },
  sectionHeader: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 12 },
  sectionTitle: { color: colors.gold, fontSize: 14, fontWeight: 'bold' },
  historyBtn: { color: colors.info, fontSize: 12 },
  walletRow: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
  walletAddress: { color: colors.text, fontSize: 14, fontWeight: 'bold' },
  walletStatus: { color: colors.success, fontSize: 12, marginTop: 2 },
  walletBtn: {
    backgroundColor: colors.surfaceLight, borderRadius: 8,
    paddingHorizontal: 14, paddingVertical: 6,
    borderWidth: 1, borderColor: colors.border,
  },
  walletBtnText: { color: colors.text, fontSize: 12 },
  merchantBtn: {
    backgroundColor: colors.surfaceLight, borderRadius: 10,
    padding: 12, alignItems: 'center',
    borderWidth: 1, borderColor: colors.gold,
  },
  merchantBtnText: { color: colors.gold, fontSize: 14 },
  menuItem: {
    flexDirection: 'row', alignItems: 'center',
    paddingVertical: 12, gap: 12,
  },
  menuItemBorder: { borderBottomWidth: 1, borderBottomColor: colors.border },
  menuIcon: { fontSize: 18 },
  menuLabel: { flex: 1, color: colors.text, fontSize: 14 },
  menuArrow: { color: colors.textMuted, fontSize: 18 },
  logoutBtn: {
    backgroundColor: colors.surface, borderRadius: 12,
    padding: 16, alignItems: 'center', marginBottom: 20,
    borderWidth: 1, borderColor: colors.danger,
  },
  logoutText: { color: colors.danger, fontSize: 15, fontWeight: 'bold' },
});