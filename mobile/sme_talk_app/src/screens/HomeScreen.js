import React, { useEffect, useState } from 'react';
import {
  View, Text, ScrollView, StyleSheet, ActivityIndicator
} from 'react-native';
import colors from '../theme/colors';
import GoldCard from '../components/GoldCard';
import ESGScoreBar from '../components/ESGScoreBar';
import BottomNav from '../components/BottomNav';

export default function HomeScreen({ user, onNavigate }) {
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchSummary();
  }, []);

  const fetchSummary = () => {
    setSummary({
      balance: 3250,
      asaId: '12345678',
      eScore: 72,
      sScore: 65,
      gScore: 58,
      policyAlert: '이번 주 환경 활동 보상 1.2배 상향 적용 중',
      recentActivities: [
        { type: '🌿 환경', desc: '다회용 컵 사용 인증', reward: '+50 ESGG', time: '오늘 14:32' },
        { type: '🚴 사회', desc: '자전거 이동 3.2km', reward: '+32 ESGG', time: '오늘 09:15' },
        { type: '🌿 환경', desc: '장바구니 지참 인증', reward: '+30 ESGG', time: '어제 17:44' },
      ],
    });
    setLoading(false);
  };

  if (loading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator color={colors.gold} size="large" />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <ScrollView style={styles.scroll} showsVerticalScrollIndicator={false}>
        <View style={styles.header}>
          <View>
            <Text style={styles.greeting}>안녕하세요 👋</Text>
            <Text style={styles.userName}>{user?.name || '사용자'}님</Text>
          </View>
          <Text style={styles.bell}>🔔</Text>
        </View>

        <GoldCard
          balance={summary.balance}
          asaId={summary.asaId}
          onSend={() => onNavigate('wallet')}
          onReceive={() => onNavigate('wallet')}
          onExchange={() => onNavigate('wallet')}
        />

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>ESG 활동 점수</Text>
          <ESGScoreBar
            e={summary.eScore}
            s={summary.sScore}
            g={summary.gScore}
          />
        </View>

        {summary.policyAlert && (
          <View style={styles.alertBanner}>
            <Text style={styles.alertIcon}>🤖</Text>
            <Text style={styles.alertText}>{summary.policyAlert}</Text>
          </View>
        )}

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>최근 활동</Text>
          {summary.recentActivities.map((item, index) => (
            <View key={index} style={styles.activityItem}>
              <View>
                <Text style={styles.activityType}>{item.type}</Text>
                <Text style={styles.activityDesc}>{item.desc}</Text>
                <Text style={styles.activityTime}>{item.time}</Text>
              </View>
              <Text style={styles.activityReward}>{item.reward}</Text>
            </View>
          ))}
        </View>
      </ScrollView>

      <BottomNav active="home" onPress={onNavigate} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.bg },
  center: { flex: 1, backgroundColor: colors.bg, alignItems: 'center', justifyContent: 'center' },
  scroll: { flex: 1, padding: 20 },
  header: {
    flexDirection: 'row', justifyContent: 'space-between',
    alignItems: 'center', marginBottom: 20,
  },
  greeting: { color: colors.textMuted, fontSize: 13 },
  userName: { color: colors.text, fontSize: 20, fontWeight: 'bold' },
  bell: { fontSize: 24 },
  section: {
    backgroundColor: colors.surface, borderRadius: 16,
    padding: 16, marginTop: 16,
    borderWidth: 1, borderColor: colors.border,
  },
  sectionTitle: {
    color: colors.gold, fontSize: 14,
    fontWeight: 'bold', marginBottom: 12,
  },
  alertBanner: {
    flexDirection: 'row', alignItems: 'center',
    backgroundColor: colors.surfaceLight, borderRadius: 12,
    padding: 12, marginTop: 16, gap: 8,
    borderLeftWidth: 3, borderLeftColor: colors.gold,
  },
  alertIcon: { fontSize: 18 },
  alertText: { color: colors.text, fontSize: 13, flex: 1 },
  activityItem: {
    flexDirection: 'row', justifyContent: 'space-between',
    alignItems: 'center', paddingVertical: 10,
    borderBottomWidth: 1, borderBottomColor: colors.border,
  },
  activityType: { color: colors.gold, fontSize: 12, fontWeight: 'bold' },
  activityDesc: { color: colors.text, fontSize: 13, marginVertical: 2 },
  activityTime: { color: colors.textMuted, fontSize: 11 },
  activityReward: { color: colors.success, fontSize: 14, fontWeight: 'bold' },
});