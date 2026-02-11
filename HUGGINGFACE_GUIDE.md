# Hugging Face LLM Integration Guide

## Overview

AnalytIQ uses Hugging Face Inference API to generate AI-powered insights from data analysis results. The system uses the Mistral-7B-Instruct model for generating business-focused insights.

## Model Selection

**Current Model:** `mistralai/Mistral-7B-Instruct-v0.2`

**Why Mistral-7B?**
- Excellent instruction following
- Strong reasoning capabilities
- Good balance of speed and quality
- Free tier available on Hugging Face

**Alternative Models:**
- `meta-llama/Llama-2-7b-chat-hf` - Good for conversational insights
- `google/flan-t5-xxl` - Faster, lighter weight
- `mistralai/Mixtral-8x7B-Instruct-v0.1` - More powerful, slower

## Getting API Key

1. Create account at https://huggingface.co
2. Go to Settings → Access Tokens
3. Create new token with "Read" permission
4. Copy token to `.env` file:
   ```
   HUGGINGFACE_API_KEY=hf_xxxxxxxxxxxxxxxxxxxxx
   ```

## Prompt Engineering

### Current Prompt Template

```python
prompt = f"""You are a senior data analyst. Analyze this dataset and provide business insights.

Dataset Overview:
- Rows: {rows}
- Columns: {columns}
- Data Quality: {completeness}% complete

Data Cleaning:
- Missing values handled: {missing_columns} columns
- Duplicates removed: {duplicates}
- Outliers detected: {outlier_columns} columns

Provide 3-5 key insights about data quality, patterns, and recommended next steps:"""
```

### Prompt Design Principles

1. **Clear Role Definition:** "You are a senior data analyst"
2. **Structured Input:** Organized data summary
3. **Specific Instructions:** "Provide 3-5 key insights"
4. **Business Focus:** Emphasize actionable recommendations

### Advanced Prompt Examples

#### For Time-Series Data
```python
prompt = f"""You are a senior data analyst specializing in time-series analysis.

Dataset: {filename}
Time Range: {start_date} to {end_date}
Frequency: {frequency}
Trend: {trend_direction}

Analyze the temporal patterns and provide:
1. Trend analysis
2. Seasonality insights
3. Anomaly detection results
4. Forecasting recommendations
"""
```

#### For Customer Segmentation
```python
prompt = f"""You are a customer analytics expert.

Dataset: {filename}
Customer Count: {customer_count}
Features: {feature_list}
Segments Identified: {num_segments}

Provide insights on:
1. Customer segment characteristics
2. High-value customer patterns
3. Churn risk indicators
4. Marketing recommendations
"""
```

#### For Financial Data
```python
prompt = f"""You are a financial data analyst.

Dataset: {filename}
Metrics: {metric_list}
Correlations: {top_correlations}
Outliers: {outlier_summary}

Analyze and provide:
1. Financial health indicators
2. Risk factors
3. Performance trends
4. Investment recommendations
"""
```

## API Configuration

### Request Parameters

```python
payload = {
    "inputs": prompt,
    "parameters": {
        "max_new_tokens": 500,      # Length of response
        "temperature": 0.7,          # Creativity (0.0-1.0)
        "top_p": 0.95,              # Nucleus sampling
        "top_k": 50,                # Top-k sampling
        "repetition_penalty": 1.2,  # Avoid repetition
        "do_sample": True           # Enable sampling
    }
}
```

### Parameter Tuning

**Temperature:**
- `0.1-0.3`: Focused, deterministic (good for factual analysis)
- `0.7-0.9`: Balanced creativity and accuracy (recommended)
- `1.0+`: Very creative, less predictable

**Max Tokens:**
- `200-300`: Brief insights
- `500-700`: Detailed analysis (recommended)
- `1000+`: Comprehensive reports

## Error Handling

### Rate Limiting
```python
try:
    response = requests.post(api_url, headers=headers, json=payload, timeout=30)
    if response.status_code == 429:
        # Rate limited - wait and retry
        time.sleep(60)
        response = requests.post(api_url, headers=headers, json=payload, timeout=30)
except requests.exceptions.Timeout:
    # Fallback to rule-based insights
    return generate_fallback_insights()
```

### Model Loading
```python
if response.status_code == 503:
    # Model is loading - retry after delay
    time.sleep(20)
    response = requests.post(api_url, headers=headers, json=payload, timeout=30)
```

## Fallback Strategy

When Hugging Face API is unavailable, the system uses rule-based insights:

```python
def _generate_fallback_insights(self, cleaning_report, eda_results):
    insights = []
    
    # Data quality insight
    completeness = eda_results.get("data_quality", {}).get("completeness", 0)
    insights.append(f"📊 Dataset has {completeness:.1f}% data completeness")
    
    # Cleaning actions
    if cleaning_report.get('missing_values'):
        insights.append(f"🔧 Handled missing values in {len(cleaning_report['missing_values'])} columns")
    
    # Outliers
    if cleaning_report.get('outliers_detected'):
        insights.append(f"⚠️ Detected outliers in {len(cleaning_report['outliers_detected'])} columns")
    
    # Recommendations
    insights.append("💡 Consider ML models or BI dashboards for deeper analysis")
    
    return "\n\n".join(insights)
```

## Cost Optimization

### Free Tier Limits
- Hugging Face Inference API: ~30,000 characters/month free
- Rate limit: ~1 request/second

### Optimization Strategies

1. **Cache Results:** Store insights for identical datasets
2. **Batch Processing:** Combine multiple analyses
3. **Prompt Compression:** Minimize prompt length
4. **Selective Usage:** Only use LLM for complex datasets

### Caching Implementation
```python
import hashlib
import json

def get_cache_key(cleaning_report, eda_results):
    data = json.dumps({"cleaning": cleaning_report, "eda": eda_results}, sort_keys=True)
    return hashlib.md5(data.encode()).hexdigest()

async def generate_insights_with_cache(self, cleaning_report, eda_results):
    cache_key = get_cache_key(cleaning_report, eda_results)
    
    # Check cache
    cached = await db.insights_cache.find_one({"key": cache_key})
    if cached:
        return cached["insights"]
    
    # Generate new insights
    insights = self.generate_insights(cleaning_report, eda_results)
    
    # Store in cache
    await db.insights_cache.insert_one({
        "key": cache_key,
        "insights": insights,
        "created_at": datetime.utcnow()
    })
    
    return insights
```

## Advanced Features

### Multi-Language Support
```python
prompt = f"""You are a senior data analyst. Respond in {language}.

Dataset Overview:
...
"""
```

### Custom Insight Types
```python
insight_types = {
    "quality": "Focus on data quality issues",
    "business": "Provide business recommendations",
    "technical": "Technical analysis for data engineers",
    "executive": "Executive summary for leadership"
}

prompt = f"""You are a senior data analyst. {insight_types[insight_type]}

Dataset Overview:
...
"""
```

### Streaming Responses
```python
import requests

def stream_insights(prompt):
    response = requests.post(
        api_url,
        headers=headers,
        json={"inputs": prompt, "parameters": {"max_new_tokens": 500}},
        stream=True
    )
    
    for chunk in response.iter_content(chunk_size=8192):
        if chunk:
            yield chunk.decode('utf-8')
```

## Testing

### Test Prompt Quality
```python
test_cases = [
    {
        "name": "Small dataset",
        "rows": 100,
        "columns": 5,
        "completeness": 98.5
    },
    {
        "name": "Large dataset with issues",
        "rows": 100000,
        "columns": 50,
        "completeness": 75.2
    }
]

for test in test_cases:
    prompt = build_prompt(test)
    insights = generate_insights(prompt)
    print(f"Test: {test['name']}")
    print(f"Insights: {insights}\n")
```

## Monitoring

### Track API Usage
```python
import logging

logger = logging.getLogger(__name__)

def generate_insights(self, cleaning_report, eda_results):
    start_time = time.time()
    
    try:
        insights = self._call_huggingface_api(prompt)
        duration = time.time() - start_time
        
        logger.info(f"HF API call successful - Duration: {duration:.2f}s")
        return insights
        
    except Exception as e:
        logger.error(f"HF API call failed: {str(e)}")
        return self._generate_fallback_insights(cleaning_report, eda_results)
```

## Best Practices

1. ✅ **Always implement fallback:** Don't rely solely on external API
2. ✅ **Set timeouts:** Prevent hanging requests
3. ✅ **Cache results:** Reduce API calls and costs
4. ✅ **Monitor usage:** Track API calls and costs
5. ✅ **Validate output:** Check for hallucinations or errors
6. ✅ **User feedback:** Allow users to rate insights quality
7. ✅ **A/B testing:** Test different prompts and models

## Future Enhancements

1. **Fine-tuning:** Train custom model on domain-specific data
2. **RAG (Retrieval Augmented Generation):** Add context from knowledge base
3. **Multi-model ensemble:** Combine insights from multiple models
4. **Interactive refinement:** Allow users to ask follow-up questions
5. **Visualization suggestions:** LLM recommends specific chart types

## Resources

- [Hugging Face Inference API Docs](https://huggingface.co/docs/api-inference/index)
- [Mistral AI Documentation](https://docs.mistral.ai/)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- [LangChain for LLM Apps](https://python.langchain.com/)
