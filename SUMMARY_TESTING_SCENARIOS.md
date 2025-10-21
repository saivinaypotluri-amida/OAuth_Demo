# 🧪 Summary Feature - Testing Scenarios

Complete test scenarios for the summary generation feature.

---

## 📋 Prerequisites Checklist

Before testing, ensure:

- [ ] Backend running: `python main.py`
- [ ] Frontend running: `npm run dev`
- [ ] Azure OpenAI configured in Settings
- [ ] Azure OpenAI test connection successful
- [ ] (Optional) Google Workspace connected
- [ ] (Optional) Google Workspace test connection successful

---

## 🧪 Test Scenario 1: Basic Web Portal Summary

**Objective:** Generate a simple summary via web portal

### Steps:

1. **Navigate to Messages page**
   ```
   http://localhost:3000/messages
   ```

2. **Click "Generate Summary" button**
   - Green button in top-right corner
   - Modal should open

3. **Fill in the form:**
   - **Title:** "Test Summary #1"
   - **Content:**
     ```
     The quarterly business review revealed strong performance across 
     all departments. Sales exceeded targets by 15%, with particularly 
     strong growth in the enterprise segment. The product team launched 
     three major features that received positive customer feedback. 
     Engineering reduced bug reports by 40% through improved testing 
     processes. Marketing's new campaign generated a 25% increase in 
     qualified leads. Looking ahead to Q4, the company plans to expand 
     into two new markets and hire 20 additional team members across 
     engineering and sales.
     ```

4. **Click "Generate & Save to Drive"**

### Expected Results:

- ✅ Loading indicator shows "Generating..."
- ✅ Summary appears within 3-5 seconds
- ✅ Summary is concise (2-4 sentences)
- ✅ Google Drive link displayed (if configured)
- ✅ Tokens used displayed
- ✅ Success message shows
- ✅ Modal stays open for 5 seconds then closes

### Example Summary Output:

```
Q3 business review showed strong performance with sales up 15% 
and 40% fewer bugs. Three new features launched successfully, 
and marketing increased qualified leads by 25%. Q4 plans include 
two new markets and 20 new hires.
```

### Verify:

1. **Go to Summaries page:**
   ```
   http://localhost:3000/summaries
   ```

2. **Check:**
   - New summary appears in list
   - Title matches: "Test Summary #1"
   - Summary text displayed
   - Google Drive link present (if configured)
   - Timestamp is recent

3. **If Google Drive configured:**
   - Click Drive link
   - Opens in new tab
   - Shows Google Doc with summary
   - Document title matches

---

## 🧪 Test Scenario 2: Slack Summary Request

**Objective:** Generate summary via Slack bot

**Prerequisites:**
- Slack real-time bot configured (see COMPLETE_SLACK_BOT_SETUP.md)
- ngrok running
- Bot added to test channel

### Steps:

1. **Open Slack workspace**

2. **Go to test channel where bot is added**

3. **Send message:**
   ```
   summarize: Climate change is one of the most pressing challenges 
   of our time. Rising global temperatures are causing more frequent 
   extreme weather events, including hurricanes, droughts, and wildfires. 
   The scientific consensus is clear that human activities, particularly 
   burning fossil fuels, are the primary cause. Solutions include 
   transitioning to renewable energy sources like solar and wind power, 
   improving energy efficiency in buildings and transportation, and 
   protecting forests that absorb carbon dioxide. While the challenge 
   is significant, many countries and companies are making commitments 
   to reduce emissions and achieve net-zero goals by 2050.
   ```

4. **Wait for bot response**

### Expected Results:

- ✅ Bot responds within 5 seconds
- ✅ Response includes "📝 Summary Generated"
- ✅ Summary text is concise
- ✅ Google Drive link included (if configured)
- ✅ Link format: `📁 Saved to Google Drive: [URL]`

### Example Bot Response:

```
📝 Summary Generated

Climate change from fossil fuels causes extreme weather events. 
Solutions include renewable energy, efficiency improvements, and 
forest protection. Many entities commit to net-zero by 2050.

📁 Saved to Google Drive: https://docs.google.com/document/d/abc123...
```

### Verify:

1. **Click Google Drive link**
   - Opens document in Drive
   - Title: "Slack Summary - [channel_name]"
   - Contains summary text

2. **Check portal Summaries page**
   - Summary appears there too
   - Same content as Slack

3. **Check backend logs**
   ```
   INFO: Processing message from user...
   INFO: Successfully generated summary via mention...
   ```

---

## 🧪 Test Scenario 3: Slack @Mention Summary

**Objective:** Use @mention to request summary

### Steps:

1. **In Slack channel:**
   ```
   @YourBot summarize: The history of the internet begins in the 1960s 
   with the development of ARPANET, a project funded by the U.S. 
   Department of Defense. The first message was sent in 1969 between 
   two computers at different universities. In the 1980s, Tim Berners-Lee 
   invented the World Wide Web at CERN, making the internet accessible 
   to the general public. The 1990s saw explosive growth with the 
   introduction of web browsers like Netscape and Internet Explorer. 
   The 2000s brought social media platforms like Facebook and Twitter, 
   fundamentally changing how people communicate. Today, billions of 
   people worldwide use the internet for work, education, entertainment, 
   and social connection.
   ```

### Expected Results:

- ✅ Bot responds with summary
- ✅ Includes Drive link
- ✅ Summary is relevant and accurate

---

## 🧪 Test Scenario 4: Alternative Keywords

**Objective:** Test different summary keywords

### Test Each Keyword:

**Test 4a: "summary"**
```
summary: [paste test text]
```

**Test 4b: "tldr"**
```
tldr: [paste test text]
```

**Test 4c: "tl;dr"**
```
tl;dr: [paste test text]
```

**Test 4d: British spelling**
```
summarise: [paste test text]
```

### Expected:

- ✅ All keywords work identically
- ✅ All generate summaries
- ✅ All save to Drive

---

## 🧪 Test Scenario 5: Short Content Error

**Objective:** Verify error handling for insufficient content

### Steps:

1. **In Slack:**
   ```
   summarize: This is too short
   ```

### Expected Results:

- ✅ Bot responds with helpful error
- ✅ Error message:
  ```
  Please provide more content to summarize. 
  Example: `summarize: [your long text here]`
  ```

### Also Test in Portal:

1. **Messages → Generate Summary**
2. **Content:** "Short text"
3. **Try to submit**

### Expected:

- ✅ Button disabled (content < 50 characters)
- ✅ Helper text shows: "Minimum 50 characters required"

---

## 🧪 Test Scenario 6: Without Google Drive

**Objective:** Verify summary works without Drive configured

### Steps:

1. **Disconnect Google Workspace:**
   - Settings → Google Workspace
   - Remove credentials (optional)

2. **Generate summary via portal:**
   - Messages → Generate Summary
   - Paste long text
   - Generate

### Expected Results:

- ✅ Summary still generates
- ✅ Summary text displayed
- ✅ Saved to database
- ✅ **No Google Drive link** (this is normal)
- ✅ No errors shown

### Verify:

- Summary appears in Summaries page
- `google_drive_file_url` is null
- Everything else works

---

## 🧪 Test Scenario 7: Multiple Summaries

**Objective:** Generate several summaries and verify tracking

### Steps:

1. **Generate 5 different summaries**
   - Use web portal or Slack
   - Different content each time
   - Different titles

2. **Check Summaries page:**
   ```
   http://localhost:3000/summaries
   ```

### Expected Results:

- ✅ All 5 summaries listed
- ✅ Sorted by date (newest first)
- ✅ Each has unique title
- ✅ Each has Drive link (if configured)
- ✅ Creation timestamps different

3. **Check Dashboard:**
   ```
   http://localhost:3000/dashboard
   ```

### Expected:

- ✅ Summary count increased by 5
- ✅ Token usage increased
- ✅ Stats updated

4. **Check Admin Logs:**
   ```
   http://localhost:3000/admin/logs
   ```

### Expected:

- ✅ 5 "generate_summary" actions
- ✅ All show "success" status
- ✅ Timestamps match

---

## 🧪 Test Scenario 8: Long Content

**Objective:** Test with very long content (stress test)

### Steps:

1. **Generate summary with 1000+ word content**
   - Use a full article or long document
   - Paste into portal

2. **Click Generate**

### Expected Results:

- ✅ Takes 5-10 seconds (longer than usual)
- ✅ Summary still concise (not proportionally long)
- ✅ Higher token usage
- ✅ Successfully completes

### Monitor:

- Token count (should be higher)
- Cost calculation
- Response time

---

## 🧪 Test Scenario 9: Special Characters

**Objective:** Verify handling of special characters

### Steps:

1. **Content with:**
   - Emojis: 🚀 💡 ✅
   - Symbols: &, @, #, $, %
   - Quotes: "text" and 'text'
   - Line breaks and formatting

2. **Generate summary**

### Expected:

- ✅ Handles gracefully
- ✅ Summary is clean
- ✅ No encoding errors

---

## 🧪 Test Scenario 10: Concurrent Requests

**Objective:** Test multiple simultaneous summary requests

### Steps:

1. **Open 2 browser tabs**

2. **In both tabs simultaneously:**
   - Messages → Generate Summary
   - Paste different content
   - Click Generate at same time

3. **Also in Slack:**
   - Send summary request

### Expected Results:

- ✅ All 3 requests complete successfully
- ✅ No conflicts or errors
- ✅ Each gets unique summary
- ✅ All saved correctly

---

## 📊 Performance Benchmarks

### Typical Performance:

| Metric | Target | Typical |
|--------|--------|---------|
| Response Time | < 10s | 2-5s |
| Summary Length | 2-5 sentences | 3 sentences |
| Token Usage | 200-500 | ~350 |
| Cost per Summary | < $0.01 | ~$0.002 |
| Drive Upload | < 3s | 1-2s |

---

## ✅ Complete Test Checklist

### Web Portal:

- [ ] Basic summary generation
- [ ] With Google Drive configured
- [ ] Without Google Drive configured
- [ ] Short content error handling
- [ ] Long content (1000+ words)
- [ ] Special characters
- [ ] View in Summaries page
- [ ] Click Drive link opens document
- [ ] Stats update in Dashboard

### Slack:

- [ ] Direct summary request: `summarize:`
- [ ] @Mention summary: `@bot summarize:`
- [ ] Alternative keyword: `tldr:`
- [ ] Alternative keyword: `summary:`
- [ ] Short content error
- [ ] Bot responds within 5 seconds
- [ ] Drive link in response
- [ ] Summary appears in portal too

### Data & Tracking:

- [ ] Summaries saved to database
- [ ] Google Drive documents created
- [ ] Usage stats updated
- [ ] Audit logs created
- [ ] Token usage tracked
- [ ] Cost calculated
- [ ] Timestamps accurate

### Edge Cases:

- [ ] Very long content
- [ ] Very short content
- [ ] Special characters
- [ ] Multiple simultaneous requests
- [ ] No internet connection (error handling)
- [ ] Azure OpenAI down (error handling)

---

## 🐛 Common Issues & Solutions

### Issue: "Azure AI not configured"

**Solution:**
```
1. Settings → Azure OpenAI Configuration
2. Enter endpoint, key, deployment
3. Test Connection
4. Should show success ✅
```

---

### Issue: Summary not saving to Drive

**Check:**
- Google Workspace configured?
- Google connection tested?
- Check error logs in backend

**If not configured:**
- Summary still works ✅
- Just no Drive link
- Configure Drive if needed

---

### Issue: Slow response time (> 10s)

**Causes:**
- Very long content
- Slow Azure OpenAI region
- Network latency

**Solutions:**
- Use shorter content
- Check Azure region
- Monitor network

---

### Issue: Summary too long or too short

**Note:** AI decides summary length based on content

**Expected:**
- Input: 500 words → Summary: 50-100 words
- Input: 1000 words → Summary: 75-150 words

**If unsatisfied:**
- Try rephrasing prompt (future enhancement)

---

## 🎯 Success Criteria

**All tests pass if:**

✅ **Functionality:**
- Summaries generate successfully
- Google Drive integration works
- Both portal and Slack work
- Error handling graceful

✅ **Performance:**
- Response time < 10 seconds
- No crashes or hangs
- Handles concurrent requests

✅ **Data:**
- All summaries saved
- Stats updated correctly
- Audit logs complete
- Drive links valid

✅ **User Experience:**
- Clear success/error messages
- Intuitive UI
- Fast enough for real use
- Drive links clickable

---

**Ready to test? Start with Test Scenario 1!** 🧪✨
