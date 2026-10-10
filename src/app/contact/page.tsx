"use client";

import React, { useState } from 'react';
import Link from 'next/link';

export default function ContactPage() {
  const [submitted, setSubmitted] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    orderNumber: '',
    inquiryType: 'general',
    message: '',
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitted(true);
  };

  return (
    <div style={{ maxWidth: '860px', margin: '0 auto', padding: '3.5rem 1.5rem', color: 'var(--foreground)' }}>
      <div style={{ textAlign: 'center', marginBottom: '3rem' }}>
        <span style={{ fontSize: '0.82rem', fontWeight: 800, color: 'var(--accent-gold)', letterSpacing: '0.12em', textTransform: 'uppercase' }}>
          Customer Support // Concierge
        </span>
        <h1 style={{ fontSize: '2.5rem', fontWeight: 900, marginTop: '0.5rem', marginBottom: '0.75rem', letterSpacing: '-0.02em' }}>
          Contact Us
        </h1>
        <p style={{ color: 'var(--text-muted)', fontSize: '1.05rem', maxWidth: '600px', margin: '0 auto' }}>
          Have a question regarding custom gamertag personalization, jobsite workwear, B2B volume pricing, or order tracking? We are here to help.
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))', gap: '1.25rem', marginBottom: '2.5rem' }}>
        <div style={{ background: 'rgba(255, 255, 255, 0.03)', border: '1px solid rgba(255, 255, 255, 0.08)', borderRadius: '10px', padding: '1.5rem', textAlign: 'center' }}>
          <div style={{ fontSize: '1.8rem', marginBottom: '0.5rem' }}>✉️</div>
          <div style={{ fontWeight: 700, fontSize: '1rem', color: '#fff' }}>Direct Email</div>
          <div style={{ color: 'var(--accent-gold)', fontSize: '0.92rem', marginTop: '0.25rem', fontWeight: 600 }}>support@krownsupplyco.com</div>
          <div style={{ color: 'var(--text-muted)', fontSize: '0.8rem', marginTop: '0.25rem' }}>Mon–Fri • Responds &lt; 24h</div>
        </div>

        <div style={{ background: 'rgba(255, 255, 255, 0.03)', border: '1px solid rgba(255, 255, 255, 0.08)', borderRadius: '10px', padding: '1.5rem', textAlign: 'center' }}>
          <div style={{ fontSize: '1.8rem', marginBottom: '0.5rem' }}>👑</div>
          <div style={{ fontWeight: 700, fontSize: '1rem', color: '#fff' }}>B2B Custom Hat Inquiries</div>
          <div style={{ color: 'var(--accent-gold)', fontSize: '0.92rem', marginTop: '0.25rem', fontWeight: 600 }}>b2b@krownsupplyco.com</div>
          <div style={{ color: 'var(--text-muted)', fontSize: '0.8rem', marginTop: '0.25rem' }}>Trade crews, esports orgs, fleet orders</div>
        </div>

        <div style={{ background: 'rgba(255, 255, 255, 0.03)', border: '1px solid rgba(255, 255, 255, 0.08)', borderRadius: '10px', padding: '1.5rem', textAlign: 'center' }}>
          <div style={{ fontSize: '1.8rem', marginBottom: '0.5rem' }}>⚡</div>
          <div style={{ fontWeight: 700, fontSize: '1rem', color: '#fff' }}>Fulfillment Hubs</div>
          <div style={{ color: '#e5e7eb', fontSize: '0.92rem', marginTop: '0.25rem', fontWeight: 600 }}>US Regional Production</div>
          <div style={{ color: 'var(--text-muted)', fontSize: '0.8rem', marginTop: '0.25rem' }}>Certified print &amp; embroidery centers</div>
        </div>
      </div>

      <div style={{ background: 'rgba(255, 255, 255, 0.03)', border: '1px solid rgba(255, 255, 255, 0.08)', borderRadius: '12px', padding: '2rem' }}>
        {submitted ? (
          <div style={{ textAlign: 'center', padding: '2rem 1rem' }}>
            <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>✓</div>
            <h2 style={{ fontSize: '1.5rem', fontWeight: 800, color: '#39FF14', marginBottom: '0.5rem' }}>
              Message Received!
            </h2>
            <p style={{ color: '#d1d5db', fontSize: '0.95rem', maxWidth: '480px', margin: '0 auto 1.5rem' }}>
              Thank you for contacting KrowN Supply Co. A customer care representative will review your message and reply to <strong>{formData.email}</strong> within 24 hours.
            </p>
            <button 
              type="button"
              onClick={() => { setSubmitted(false); setFormData({ name: '', email: '', orderNumber: '', inquiryType: 'general', message: '' }); }}
              style={{ background: 'var(--accent-gold)', color: '#000', fontWeight: 700, padding: '0.65rem 1.5rem', borderRadius: '6px', border: 'none', cursor: 'pointer' }}
            >
              Send Another Message
            </button>
          </div>
        ) : (
          <form onSubmit={handleSubmit}>
            <h2 style={{ fontSize: '1.3rem', fontWeight: 800, color: '#fff', marginBottom: '1.5rem' }}>
              Send an Instant Inquiry
            </h2>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '1rem', marginBottom: '1rem' }}>
              <div>
                <label style={{ display: 'block', fontSize: '0.82rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '0.35rem' }}>
                  Full Name *
                </label>
                <input 
                  type="text" 
                  required 
                  value={formData.name}
                  onChange={e => setFormData({ ...formData, name: e.target.value })}
                  placeholder="e.g. John Doe"
                  style={{ width: '100%', padding: '0.75rem', borderRadius: '6px', border: '1px solid rgba(255, 255, 255, 0.15)', background: 'rgba(0, 0, 0, 0.4)', color: '#fff', fontSize: '0.92rem' }}
                />
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '0.82rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '0.35rem' }}>
                  Email Address *
                </label>
                <input 
                  type="email" 
                  required 
                  value={formData.email}
                  onChange={e => setFormData({ ...formData, email: e.target.value })}
                  placeholder="name@example.com"
                  style={{ width: '100%', padding: '0.75rem', borderRadius: '6px', border: '1px solid rgba(255, 255, 255, 0.15)', background: 'rgba(0, 0, 0, 0.4)', color: '#fff', fontSize: '0.92rem' }}
                />
              </div>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '1rem', marginBottom: '1rem' }}>
              <div>
                <label style={{ display: 'block', fontSize: '0.82rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '0.35rem' }}>
                  Order Number (If applicable)
                </label>
                <input 
                  type="text" 
                  value={formData.orderNumber}
                  onChange={e => setFormData({ ...formData, orderNumber: e.target.value })}
                  placeholder="e.g. #KRW-10492"
                  style={{ width: '100%', padding: '0.75rem', borderRadius: '6px', border: '1px solid rgba(255, 255, 255, 0.15)', background: 'rgba(0, 0, 0, 0.4)', color: '#fff', fontSize: '0.92rem' }}
                />
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '0.82rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '0.35rem' }}>
                  Inquiry Topic *
                </label>
                <select 
                  value={formData.inquiryType}
                  onChange={e => setFormData({ ...formData, inquiryType: e.target.value })}
                  style={{ width: '100%', padding: '0.75rem', borderRadius: '6px', border: '1px solid rgba(255, 255, 255, 0.15)', background: '#18191e', color: '#fff', fontSize: '0.92rem' }}
                >
                  <option value="general">General Inquiry</option>
                  <option value="order">Order Status &amp; Tracking</option>
                  <option value="custom">Custom Gamertag / Artwork Proof</option>
                  <option value="defect">Damaged / Defective Replacement</option>
                  <option value="b2b">B2B Custom Hat Fleet Order</option>
                </select>
              </div>
            </div>

            <div style={{ marginBottom: '1.5rem' }}>
              <label style={{ display: 'block', fontSize: '0.82rem', fontWeight: 600, color: 'var(--text-muted)', marginBottom: '0.35rem' }}>
                Your Message *
              </label>
              <textarea 
                required 
                rows={5}
                value={formData.message}
                onChange={e => setFormData({ ...formData, message: e.target.value })}
                placeholder="Please describe how we can help you..."
                style={{ width: '100%', padding: '0.75rem', borderRadius: '6px', border: '1px solid rgba(255, 255, 255, 0.15)', background: 'rgba(0, 0, 0, 0.4)', color: '#fff', fontSize: '0.92rem', resize: 'vertical' }}
              />
            </div>

            <button 
              type="submit" 
              style={{ 
                width: '100%', 
                background: 'var(--accent-gold)', 
                color: '#000', 
                fontWeight: 800, 
                fontSize: '1rem', 
                padding: '0.9rem', 
                borderRadius: '6px', 
                border: 'none', 
                cursor: 'pointer' 
              }}
            >
              Submit Support Ticket &rarr;
            </button>
          </form>
        )}
      </div>
    </div>
  );
}
