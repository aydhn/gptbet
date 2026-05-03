# Phase 72: Bounded Live Execution, Rollback, and Supervised Closure

## Bounded Live Execution Katmanının Amacı
Bu katman, lane tabanlı düzeltme ve remediation (iyileştirme) akışlarını güvenli bir kapalı döngü içerisinde canlı sistemde çalıştırmayı sağlar. Amaç, sınırsız self-healing değil; açıkça onaylanmış pencerelerde, gözlemlenebilen ve güvenli bir şekilde kapatılabilen, hata anında rollback yapabilen dar kapsamlı canlı execution omurgası oluşturmaktır.

## Temel Farklar
*   **Runtime:** İşlem limitleri olan, geçici bir yürütme (execution) yetkisi sağlayan motor.
*   **Token Renewal:** Kullanım süresi dolmak üzere olan çalışma yetkisinin yeniden alınması, bu durum asla kapsamı (scope) genişletemez.
*   **Rollback Automaton:** Her çalışma durumunun hata oluştuğunda nasıl eski haline döndürüleceğini kontrol eden geri dönüş (rollback) sistemi.
*   **Closure Controller:** İşlem bittiğinde gözlem ve checkpoint'leri denetleyip, bitişin (completion) gerçekten başarılı olup olmadığını, "supervised closure" ile kanıtlayan denetçi.

## CLI Commands
- `python -m sports_signal_bot.main live-execution run-live-execution-pass`
- `python -m sports_signal_bot.main live-execution list-live-execution-strategies`

## Mimari Prensipler
- **Neden tokenlar kullanıyoruz:** Tokenlar sadece kısa bir iş penceresini yetkilendirir, genel bir otomasyon yetkisi vermez.
- **Neden closure zorunlu:** Yalnızca çalışan değil, beklendiği gibi çalıştığı kanıtlanabilen execution'lar 'completion_verified' statüsünü kazanır. Supervised closure, sistemin arkada bozukluk bırakmasını engeller.
