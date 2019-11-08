# Issue Tracker

## When will MTR close today?

- TODO: deal with potential issue raised by timezone. Handle comparison between naive datetime and aware datetime.

- TODO: add unit test

- TODO: add iOS workflow support

- TODO: correctness problem: sometimes the release date of the train service info or the date in the tsi_title are not necessarily the same with the close date the sliding text is talking about. E.g.:

  ```html
  <div
    id="TSI_629"
    class="col12 last Tcol12 Mcol12 dpids_content flip-alert"
    style="position: absolute; top: 0px; left: -1160px; display: none; z-index: 2; opacity: 1; width: 100%;"
  >
    <a name="629"> </a>
    <div class="title_extension title_sign3 tsi_title">
      <table>
        <tbody>
          <tr>
            <td>
              <div style="float:left;width:40px;margin: 0px 15px 0px 15px;">
                <img
                  src="./image/ui/ico_speaker_bak.png"
                  style="image-rendering: -moz-crisp-edges;image-rendering: -o-crisp-edges;image-rendering: -webkit-optimize-contrast;-ms-interpolation-mode: nearest-neighbor;"
                />
              </div>
            </td>
            <td>
              <strong>港鐵列車服務安排（10月31日）</strong>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="clear"></div>
    <br />
    <div style="float:left;color: #000000;">
      此訊息發放時間 : 2019-11-01 01:20
    </div>
    <div class="clear"></div>
    <br />
    <div class="line_data"></div>
    <div class="content_text">
      <strong></strong>
    </div>

    <div id="sliding629">
      <p></p>
      <p>
        港鐵各綫、機場快綫、輕鐵及港鐵巴士今天的服務時間已經完結。<br />
        <br />
        雖然多項被破壞的設施仍有待復修，但經港鐵維修人員的努力，設施的復修進度有所改善，而與相關政府部門進行風險評估後，明天(11月1日)港鐵各綫(機場快綫除外)、輕鐵及港鐵巴士服務將於晚上11時結束。<br />
        <br />
        我們會繼續評估風險狀況，並有可能因應風險增加或再有鐵路設施被破壞而縮短服務時間。
      </p>
      <p></p>
      <br />
      <p></p>
      <br />
    </div>
    <br /><br /><br /><br />

    <div class="back_to_homepage">
      <a>
        <button
          type="button"
          id="footerbtn_629"
          onclick="window.location='http://www.mtr.com.hk/?notice=read&amp;gLang=C';"
        >
          &lt; 返回主頁
        </button>
      </a>
    </div>
    <br /><br /><br /><br /><br /><br />
  </div>
  ```

- TODO: provide integration with IFTTT

- Add type checking based on type hint. These checking are necessary since their corresponding type-checking logic code are intentionally left not written.
