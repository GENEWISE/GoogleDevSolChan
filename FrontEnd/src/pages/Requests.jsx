import React, { useState } from 'react';
import {
  FileText, User, CheckCircle, XCircle, Search, ArrowDownLeft,
  ArrowUpRight, Plus, AlertCircle, FileCheck, Calendar, Bell,
  Settings, LogOut
} from 'lucide-react';

function Requests() {
  const [activeTab, setActiveTab] = useState('incoming');
  const [showAddModal, setShowAddModal] = useState(false);
  const [showNotifications, setShowNotifications] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');

  const [requests] = useState([
    {
      id: '1',
      patientName: 'John Smith',
      requestingDoctor: 'Dr. Sarah Wilson',
      owningDoctor: 'Dr. James Miller',
      documentType: 'Medical History',
      urgency: 'High',
      status: 'Pending',
      requestDate: '2024-03-15',
      description: 'Complete medical history including recent cardiovascular examination results',
      avatar: 'https://images.unsplash.com/photo-1559839734-2b71ea197ec2?w=150&h=150&fit=crop'
    },
    {
      id: '2',
      patientName: 'Emma Johnson',
      requestingDoctor: 'Dr. Michael Chen',
      owningDoctor: 'Dr. James Miller',
      documentType: 'Lab Results',
      urgency: 'Medium',
      status: 'Pending',
      requestDate: '2024-03-14',
      description: 'Blood work results from annual checkup',
      avatar: 'https://images.unsplash.com/photo-1573497019940-1c28c88b4f3e?w=150&h=150&fit=crop'
    },
    {
      id: '3',
      patientName: 'Robert Davis',
      requestingDoctor: 'Dr. James Miller',
      owningDoctor: 'Dr. Lisa Thompson',
      documentType: 'Radiology Report',
      urgency: 'High',
      status: 'Approved',
      requestDate: '2024-03-13',
      description: 'Chest X-ray results for pneumonia diagnosis',
      avatar: 'https://images.unsplash.com/photo-1566492031773-4f4e44671857?w=150&h=150&fit=crop'
    }
  ]);

  const currentDoctor = 'Dr. James Miller';

  const [notifications] = useState([
    { id: 1, message: 'New document request from Dr. Sarah Wilson', time: '5m ago' },
    { id: 2, message: 'Dr. Thompson approved your request', time: '1h ago' },
    { id: 3, message: 'Reminder: Pending request for John Smith', time: '2h ago' }
  ]);

  const filteredRequests = requests.filter(request => {
    const searchLower = searchTerm.toLowerCase();
    return (
      request.patientName.toLowerCase().includes(searchLower) ||
      request.documentType.toLowerCase().includes(searchLower) ||
      request.description.toLowerCase().includes(searchLower)
    );
  });

  const incomingRequests = filteredRequests.filter(req => req.owningDoctor === currentDoctor);
  const outgoingRequests = filteredRequests.filter(req => req.requestingDoctor === currentDoctor);

  const handleRequestAction = (id, action) => {
    console.log(`Request ${id} ${action}`);
  };

  const NotificationsPanel = () => (
    <div className="notifications-panel">
      <div className="notifications-header">
        <h3 className="notifications-title">Notifications</h3>
      </div>
      <div className="notifications-list">
        {notifications.map(notification => (
          <div key={notification.id} className="notification-item">
            <p className="notification-message">{notification.message}</p>
            <p className="notification-time">{notification.time}</p>
          </div>
        ))}
      </div>
    </div>
  );

  const AddRequestModal = () => (
    <div className="modal-overlay">
      <div className="modal">
        <div className="modal-header">
          <h3 className="modal-title">New Document Request</h3>
          <button onClick={() => setShowAddModal(false)}>
            <XCircle className="h-6 w-6" />
          </button>
        </div>
        <form className="form">
          <div className="form-group">
            <label className="form-label">Patient Name</label>
            <input type="text" className="form-input" placeholder="Enter patient name" />
          </div>
          <div className="form-group">
            <label className="form-label">Document Owner</label>
            <input type="text" className="form-input" placeholder="Search for doctor" />
          </div>
          <div className="form-group">
            <label className="form-label">Document Type</label>
            <select className="form-input">
              <option value="">Select document type</option>
              <option>Medical History</option>
              <option>Lab Results</option>
              <option>Radiology Report</option>
              <option>Prescription History</option>
              <option>Treatment Plan</option>
            </select>
          </div>
          <div className="form-group">
            <label className="form-label">Urgency</label>
            <div className="radio-group">
              {['Low', 'Medium', 'High'].map(level => (
                <label key={level} className="radio-label">
                  <input type="radio" name="urgency" value={level} />
                  <span>{level}</span>
                </label>
              ))}
            </div>
          </div>
          <div className="form-group">
            <label className="form-label">Description</label>
            <textarea className="form-input" rows={3} placeholder="Provide details about the request" />
          </div>
          <div className="form-actions">
            <button type="button" onClick={() => setShowAddModal(false)} className="btn">
              Cancel
            </button>
            <button type="submit" className="btn btn-new">
              Submit Request
            </button>
          </div>
        </form>
      </div>
    </div>
  );

  const RequestCard = ({ request }) => (
    <div className="request-card">
      <div className="card-content">
        <div className="card-header">
          <div className="patient-info">
            {request.avatar ? (
              <img src={request.avatar} alt={request.patientName} className="avatar" />
            ) : (
              <User className="avatar" />
            )}
            <div className="patient-details">
              <h3 className="patient-name">{request.patientName}</h3>
              <p className="doctor-name">
                {activeTab === 'incoming' ? request.requestingDoctor : request.owningDoctor}
              </p>
            </div>
          </div>
          <div className="status-badges">
            <span className={`badge badge-${request.urgency.toLowerCase()}`}>
              {request.urgency} Priority
            </span>
            <span className={`badge badge-${request.status.toLowerCase()}`}>
              {request.status}
            </span>
          </div>
        </div>

        <div className="document-info">
          <div className="document-type">
            <FileCheck className="h-5 w-5" />
            <span>{request.documentType}</span>
          </div>
          <p className="description">{request.description}</p>
        </div>

        <div className="card-footer">
          <div className="date">
            <Calendar className="h-4 w-4" />
            {request.requestDate}
          </div>

          {activeTab === 'incoming' && request.status === 'Pending' && (
            <div className="action-buttons">
              <button onClick={() => handleRequestAction(request.id, 'Approved')} className="btn btn-approve">
                <CheckCircle className="h-4 w-4" />
                Approve
              </button>
              <button onClick={() => handleRequestAction(request.id, 'Rejected')} className="btn btn-reject">
                <XCircle className="h-4 w-4" />
                Reject
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="header">
        <div className="header-content">
          <div className="logo-container">
            <div className="logo">
              <FileText className="h-8 w-8" />
            </div>
            <h1 className="app-title">Document Requests</h1>
          </div>
          <div className="header-actions">
            <div className="search-container">
              <Search className="search-icon" />
              <input
                type="text"
                placeholder="Search requests..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="search-input"
              />
            </div>
            <div className="relative">
              <button onClick={() => setShowNotifications(!showNotifications)} className="btn">
                <Bell className="h-6 w-6" />
                <span className="notification-indicator"></span>
              </button>
              {showNotifications && <NotificationsPanel />}
            </div>
            <button className="btn">
              <Settings className="h-6 w-6" />
            </button>
          </div>
        </div>
      </header>

      <main className="main-content">
        <div className="content-container">
          <div className="tabs">
            <button
              onClick={() => setActiveTab('incoming')}
              className={`tab ${activeTab === 'incoming' ? 'active' : ''}`}
            >
              <ArrowDownLeft className="h-5 w-5" />
              Incoming Requests ({incomingRequests.length})
            </button>
            <button
              onClick={() => setActiveTab('outgoing')}
              className={`tab ${activeTab === 'outgoing' ? 'active' : ''}`}
            >
              <ArrowUpRight className="h-5 w-5" />
              Outgoing Requests ({outgoingRequests.length})
            </button>
          </div>

          <div className="content-body">
            {activeTab === 'outgoing' && (
              <div className="new-request-container">
                <button onClick={() => setShowAddModal(true)} className="btn btn-new">
                  <Plus className="h-5 w-5" />
                  New Request
                </button>
              </div>
            )}

            <div className="request-grid">
              {(activeTab === 'incoming' ? incomingRequests : outgoingRequests).map((request) => (
                <RequestCard key={request.id} request={request} />
              ))}
            </div>

            {(activeTab === 'incoming' ? incomingRequests : outgoingRequests).length === 0 && (
              <div className="empty-state">
                <AlertCircle className="empty-icon" />
                <h3 className="empty-title">No requests found</h3>
                <p className="empty-description">
                  {activeTab === 'incoming'
                    ? "You don't have any incoming document requests."
                    : "You haven't made any document requests yet."}
                </p>
              </div>
            )}
          </div>
        </div>
      </main>

      {showAddModal && <AddRequestModal />}
    </div>
  );
}

export default Requests;
